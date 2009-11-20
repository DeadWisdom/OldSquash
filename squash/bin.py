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

