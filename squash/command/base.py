import argparse, sys, squash

Action = None

class ActionMeta(type):
    def __new__(meta, classname, bases, classDict):
        cls = type.__new__(meta, classname, bases, classDict)
        if Action is not None:
            Action.all[classDict.get('name', classname.lower())] = cls
            cls.attach(Action.parser)
        return cls

class Action(object):
    __metaclass__ = ActionMeta
    all = {}
    help = None
    general = False         # If true, this action doesn't expect to have a repo at runtime.
    parser = argparse.ArgumentParser(description='Squash project management.')
    subparsers = parser.add_subparsers(title='valid commands',
                                       dest='command')
    @classmethod
    def attach(cls, subparsers):
        cls.parser = cls.subparsers.add_parser(getattr(cls, 'name', cls.__name__.lower()), help=cls.help)
        
    @classmethod
    def add_argument(cls, *args, **kwargs):
        return cls.parser.add_argument(*args, **kwargs)
        
    def __init__(self, repo, args):
        self.repo = repo
        self.args = args
    
    def run(self, repo, args):
        pass
    
    def log(self, what, *args):
        self.args.log.write(what % args)

Action.add_argument(
        '--log', type=argparse.FileType('w'), default=sys.stdout,
        help='the file to stream the output'
             '(default: write to stdout)')
             
Action.add_argument(
        '--repo', type=str, default='.squash', help='the repository to use')
        
Action.add_argument(
        '--noinput', action='store_true', help='supress input')

def run():
    args = Action.parser.parse_args()
    
    cls = Action.all[args.command]
    if not cls.general:
        repo = squash.get_repo(args.repo)
    else:
        repo = None
    
    action = cls(repo, args)
    action.run(repo, args)
    
    if (repo is not None):
        repo.session.commit()