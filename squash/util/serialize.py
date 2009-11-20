dumpers = {}
loaders = {}
unavailable = {}

### JSON ###
try:
    import simplejson
    dumpers['json'] = simplejson.dumps
    loaders['json'] = simplejson.loads
except ImportError:
    unavailable['json'] = "The simplejson library is not found, 'easy_install simplejson' and try again."

### Yaml ###
try:
    import yaml
    try:
        from yaml import CLoader as Loader
        from yaml import CDumper as Dumper
    except:
        from yaml import Loader, Dumper
    loaders['yaml'] = lambda x: yaml.load(x, Loader=Loader)
    dumpers['yaml'] = lambda x: yaml.dump(x, Dumper=Dumper, default_flow_style=False)
except ImportError:
    unavailable['yaml'] = "The pyyaml library is not found, 'easy_install pyyaml' and try again."

### Pickle ###
try:
    import cPickle as pickle
except ImportError:
    import pickle
loaders['pickle'] = pickle.loads
dumpers['pickle'] = pickle.dumps


class SerializeError(RuntimeError):
    pass

def dump(x, format='json'):
    if format not in dumpers:
        if format in unavailable:
            raise SerializeError(unavailable[format])
        raise SerializeError("Serialize format %r is not known, options are: %s" % (format, ", ".join(dumpers.keys())))
        
    return dumpers[format](x)

def load(x, format='json'):
    if format not in loaders:
        if format in unavailable:
            raise SerializeError(unavailable[format])
        raise SerializeError("Serialize format %r is not known, options are: %s" % (format, ", ".join(loaders.keys())))
    
    return loaders[format](x)