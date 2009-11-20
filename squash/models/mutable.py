from sqlalchemy.orm.session import object_session
from squash.util.schema import DictSchema
from uuid import uuid4

def uuid():
    # TODO: Need to provide an alternative if this doesn't exist (pre 2.5)
    return str(uuid4())

def diff(a, b):
    """
    Returns the changes in b from a.
    
    >>> a = {'x': 0, 'y': 2}
    >>> b = dict(a)
    >>> b['x'] = 1
    >>> diff(a, b)
    {'x': 1}
    >>> a.update(diff(a, b))
    >>> a == b
    True
    
    """
    return dict((k, v) for k, v in b.items() if a[k] != v)

class Mutable(object):
    @property
    def session(self):
        return object_session(self)
    
    def _details(self):
        pass
        
    def _update(self, value):
        pass
    
    def details(self, key=None):
        d = {'_model': self.__class__.__name__}
        for part in self._details():
            d.update(part)
            if key is not None and key in d:
                return d
        return d
    
    def update(self, value):
        old = self.details()
        schema = self._update(value)
        
        if schema:
            schema = DictSchema(schema, all_optional=True)
            for k, v in schema(value).items():
                setattr(self, k, v)
        
        delta = diff(old, self.details())
        return delta
    
    def serialize(self, format):
        from squash.util.serialize import dump
        return dump(self.details(), format)
    
    def yaml(self):
        return self.serialize('yaml')
        