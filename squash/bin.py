#!/usr/bin/env python
import sys, os

try:
    import squash
except:
    # Not in the path, let's fix that...  Is this okay?  Seems fine to me.
    sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..')))
    import squash

if __name__ == '__main__':
    from squash.command import run
    run()

"""
    parser = argparse.ArgumentParser(description='Squash project management.')

    parser.add_argument(
        '--log', type=argparse.FileType('w'), default=sys.stdout,
        help='the file where the sum should be written '
             '(default: write the sum to stdout)')
    
    subparsers = parser.add_subparsers(title='commands',
                                       description='valid commands',
                                       help='additional help',
                                       dest='command')

    parser_abc = subparsers.add_parser('abc')
    parser_abc.add_argument('-a', action='store_true')
    parser_abc.add_argument('--b', type=int)
    parser_abc.add_argument('integers', nargs=2, type=int)

    # parse the command line
    args = parser.parse_args()

    args.log.write( "%s\n" % args.command )
    
 print dir(args)
    # write out the sum
    args.log.write('%s\n' % sum(args.integers))
    args.log.close()
"""
