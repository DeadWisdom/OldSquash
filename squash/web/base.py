import re, cgi
from squash.util import serialize

try:
    import urllib.parse
    parse_qs = urllib.parse.parse_qs
except ImportError:
    import urlparse
    parse_qs = urlparse.parse_qs


class Response(Exception):
    status = '200 OK'
    headers = [('Content-type','text/plain')]
    
    def __init__(self, content='', status=None, headers=[], name=None):
        self.headers = dict(self.headers + headers)
        self.status = status or self.status
        self.content = content
        self.name = name or self.__class__.__name__
    
    def __setitem__(self, key, value):
        return self.headers.set(key, value)
    
    def __getitem__(self, key, default):
        return self.headers.get(key, default)
    
    def __unicode__(self):
        return '%s(%s): %s' % (self.name, self.status, self.content)

class Http404(Response):
    status = '404 Not Found'


class Request(object):
    def __init__(self, environ):
        self.__dict__.update(environ)
        self.path = environ.get('PATH_INFO', '')
        self.params = parse_qs( environ['QUERY_STRING'] )
        self.method = self.params.get('method', None)
        self.format = 'json'
        if self.method:
            self.method = self.method[0].lower()
            self.input = self.params.get('input', '')
        else:
            self.method = environ.get('REQUEST_METHOD', 'get').lower()
        
        if environ.get('REQUEST_METHOD', None) in ('POST', 'PUT'):
            self.input = environ['wsgi.input'].read()


class ResourceMeta(type):
    brackets = re.compile(r'\[(\w+)\]')
    
    def __new__(meta, classname, bases, classDict):
        cls = type.__new__(meta, classname, bases, classDict)
        if cls.url:
            url = cls.url.replace('.', '\\.').replace('*', '\\*').replace('+', '\\+')
            reg = re.compile('^' + meta.brackets.sub(r'(?P<\1>\w+)', url) + '$')
            Resource.routes.append((reg, cls()))
        return cls

class Resource(object):
    __metaclass__ = ResourceMeta
    routes = []
    url = None

    def handle(self, repo, request, keywords):
        func = getattr(self, request.method, None)
        request.format = keywords.pop('format', format)
        if func:
            return func(repo, request, **keywords)
        else:
            return None


class Server(object):
    def __init__(self, repo):
        self.repo = repo
    
    def route(self, request):
        path = request.path[1:]
        for regex, resource in Resource.routes:
            m = regex.match(path)
            if m:
                request.match = m
                try:
                    repo = self.repo.manifold()
                    response = resource.handle(repo, request, request.match.groupdict())
                    repo.session.commit()
                except Response, r:
                    response = r
                if response is not None:
                    return response
        return None
    
    def process(self, environ):
        request = Request(environ)
        response = self.route(request)
        if response is None:
            content = ["Cannot %s %r\r\n\r\nAvailable:" % (request.method, environ.get('PATH_INFO')[1:])]
            for regex, resource in Resource.routes:
                for method in ('get', 'post', 'put', 'delete'):
                    func = getattr(resource, method, None)
                    if func:
                        content.append("  %-6s %-35s # %s" % (method, resource.url, func.__doc__))
            return Http404("\r\n".join(content))
        elif not isinstance(response, Response):
            return Response(
                serialize.dump(response, request.format),
                headers=[('Content-type', 'text/plain')]  # % format
            )
        else:
            return response
    
    def __call__(self, environ, start_response):
        response = self.process( environ )
        
        start_response(response.status, response.headers.items())
        if isinstance(response.content, basestring):
            yield response.content
        elif response.content:
            for i in response.content:
                yield i