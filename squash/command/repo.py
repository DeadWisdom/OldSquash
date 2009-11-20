import squash
from base import Action

class Init(Action):
    help = 'Initialize the squash repository'
    general = True
    
    def run(self, repo, args):
        repo = squash.create_repo(args.path, args.db)
        self.log("# New squash repo created: %s\n", repo.path)

Init.add_argument('path', type=str,
                          nargs='?',
                          default='.squash',
                          help='path to the repository (defaults to .squash)')

Init.add_argument('db', type=str,
                        nargs='?',
                        help='sqlalchemy url to the repository database '
                             '(defaults to "sqlite:///<path>/sqlite3.db")')


class Serve(Action):
    help = 'Serve the repository as a website.'
    
    def run(self, repo, args):
        where = args.where.split(':', 1)
        if len(where) == 1:
            where = ('localhost', int(where[0]))
        else:
            where = (where[0], int(where[1]))
        self.log("serving squash repository at %s:%s\n\n" % where)
        repo.serve(where)

Serve.add_argument('where', type=str,
                            nargs='?',
                            default='localhost:4000',
                            help='port or ip:port '
                                 '(defaults to localhost:4000)')