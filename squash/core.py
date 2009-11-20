import os
from models import Project, create_engine
from util import schema

def create_repo(path, db=None):
    return Repo(path, db)

def get_repo(path):
    if not os.path.exists(path):
        raise RuntimeError("Repo does not exist at %s" % path)
    return Repo(path)
    
class Repo(object):
    def __init__(self, path, db=None, engine=None):
        self.path = path
        self.working = None

        if not os.path.exists(path):
            os.makedirs(path)
            self.db = db or 'sqlite:///%s/sqlite3.db' % path
            self.settings_write({'DB': self.db})
        else:
            self.settings_read()
            self.db = db or self.settings['DB']
            
        self.engine = engine or create_engine(self.db, echo=False)
        self.session = self.engine.create_session()
    
    def create_project(self, slug, name='', description=''):
        if not name:
            name = slug
            slug = schema.slug(slug)
        
        p = Project(schema.slug(slug), name, description)
        self.session.add(p)
        return p
    
    def get_project(self, id):
        for column in (Project.slug, Project.name):
            project = self.session.query(Project).filter(column.like("%s%%" % id)).order_by(column).first()
            if project is not None:
                return project
        return None
    
    def get_projects(self):
        return self.session.query(Project).order_by(Project.slug)
    
    def set_working_project(self, project):
        if project is None:
            self.working = None
            open(os.path.join(self.path, 'working'), 'w').close()
            return
        
        if not isinstance(project, Project):
            project = self.get_project(project)
        
        self.working = project.slug
        
        o = open(os.path.join(self.path, 'working'), 'w')
        o.write(project.slug)
        o.write('\n')
        o.close()
        
        return project
    
    def get_working_project(self):
        if self.working is not None:
            return self.working
        
        if os.path.exists(os.path.join(self.path, 'working')):
            self.working = open(os.path.join(self.path, 'working')).read().strip()
            if (self.working):
                return self.session.query(Project).filter_by(slug=self.working).first()
        
        if (self.get_projects().count() == 1):
            return self.set_working_project( self.get_projects().first() )
            
        return None
    
    def settings_write(self, settings=None):
        settings = settings or self.settings
        o = open(os.path.join(self.path, 'settings.py'), 'w')
        o.write('# Squash settings file\n\n')
        for k, v in settings.items():
            o.write('%s = %r\n' % (k, v))
        o.close()
    
    def settings_read(self):
        self.settings = {}
        execfile(os.path.join(self.path, 'settings.py'), self.settings)
    
    def manifold(self):
        """
        Creates a copy with the same engine, but a new session.
        """
        return Repo(self.path, db=self.db, engine=self.engine)
    
    def serve(self, port=('localhost', 4000)):
        from web import Server
        try:
            from eventlet import wsgi, api
        except ImportError:
            print "Unnable to find eventlet, easy_install eventlet and try again."
            return
        
        sock = api.tcp_listener(port)
        wsgi.server(sock, Server(self))
        return sock