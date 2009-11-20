#!/usr/bin/env python

import os, sys, subprocess, StringIO, re, glob

def printf( what, args=() ):
    sys.stdout.write(what % args)
    sys.stdout.flush()

def sub_vars( str, context ):
    def repl(m):
        return context.get(m.group(1), m.group(0))
    return re.sub(r'\$(\w+)', repl, str)

def get_tests():
    tests = glob.glob('tests/*.test') + glob.glob('tests/*.py')
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
        tests = [t for t in tests if target in t]
    return tests

def get_parts( path ):
    src = "\n" + open( path ).read()
    parts = re.split(r'\n\>', src)[1:]
    return parts

def get_name( path ):
    _, filename = os.path.split(path)
    name, ext = os.path.splitext(filename)
    return name.title()
    
def test_command_line(path):
    name = get_name(path)
    exceptions = []
    context = {
        'user': os.environ['USER'],
        'squash': glob.glob('squash/bin.py')[0],
    }
    
    os.system("rm -rf .squash >/dev/null")
    
    printf("%-14s", name)
    for part in get_parts( path ):
        command, expected = part.split('\n', 1)
        expected = sub_vars(expected.strip(), context)
        command = sub_vars(command.strip(), context)
        
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            printf("E")
            exceptions.append("> %s\n%s\n%s" % (command, stdout, stderr))
            break
        else:
            if (expected.strip() != '...' and expected.strip() != stdout.strip()) or stdout.strip().startswith('Unknown command:'):
                printf("F")
                exceptions.append("> %s\n%s\n\n=== Got ===\n%s" % (command, expected, stdout))
            else:
                printf(".")
    
    if exceptions:
        print " FAILED\n"
        print "\n".join(exceptions)
    else:
        print " OK"

import types, traceback

def test_py(path):
    name = get_name(path)
    
    printf("%-14s", name)
    
    try:
        g = {}
        execfile(path, g)
        if 'setup' in g:
            g['setup']()
    except Exception, e:
        print " EXCEPTION\n"
        traceback.print_tb(sys.last_traceback)
        return
    
    exceptions = []
    
    for test in g['tests']:
        try:
            printf('\n%s\n', test.func_name)
            test()
        except Exception, e:
            exceptions.append( traceback.format_exc(sys.exc_info()[2]) )
            printf("F")
    
    if 'teardown' in g:
        g['teardown']()
    
    if exceptions:
        print " FAILED\n"
        print "\n".join(exceptions)
    else:
        print " OK"

for path in get_tests():
    if path.endswith('.test'):
        test_command_line(path)
    elif path.endswith('.py'):
        test_py(path)

