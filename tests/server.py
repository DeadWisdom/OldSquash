#!/usr/bin/env python

import sys, simplejson, os, urllib
from eventlet.green import urllib2
from eventlet.proc import spawn
from eventlet.api import sleep, exc_after

import squash

class Client(object):
    def __init__(self, port):
        self.port = port
    
    def get(self, url, params=None):
        url = 'http://localhost:%s/%s' % (self.port, url)
        if (params):
            url = '%s?%s' % (url, urllib.urlencode(params))
        try:
            o = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            e.msg = "\n".join((e.msg, e.read()))
            raise e
        return simplejson.loads(o.read())
    
    def post(self, url, value):
        try:
            o = urllib2.urlopen('http://localhost:%s/%s' % (self.port, url), simplejson.dumps(value))
        except urllib2.HTTPError, e:
            e.msg = "\n.join"((e.msg, e.read()))
            raise e
        return simplejson.loads(o.read())
    
    def put(self, url, value):
        url = '%s?method=put' % url
        self.post(url, value)

def assert_equal(a, b):
    try:
        assert a == b
    except AssertionError:
        print repr(a), '!=', repr(b)
        raise

client = None

def setup():
    global client
    primary = squash.create_repo('.primary')
    spawn(primary.serve, ('localhost', 4001))
    client = Client( 4001 )
    sleep(.1)

def test_get_projects():
    projects = client.get( '*.json' )
    assert_equal( len(projects), 0 )

def test_put_project():
    client.put( 'squash.json', {'slug': 'squash', 'name': 'Squash', 'description': 'The Squash squash.'} )
    
    projects = client.get( '*.json' )
    assert_equal( len(projects), 1 )
    assert_equal( projects[0]['slug'], 'squash' )
    
def test_get_project():
    project = client.get( 'squash.json' )
    assert_equal( project['slug'], 'squash' )
    assert_equal( project['name'], 'Squash' )
    assert_equal( project['description'], 'The Squash squash.' )

def test_post_project():
    delta = client.post( 'squash.json', {'name': 'Squish'} )
    assert_equal( delta['name'], 'Squish' )

    project = client.get( 'squash.json' )
    assert_equal( project['slug'], 'squash' )
    assert_equal( project['name'], 'Squish' )
    assert_equal( project['description'], 'The Squash squash.' )
    
def test_delete_project():
    projects = client.get( '*.json' )
    assert_equal( len(projects), 1 )
    
    response = client.get( 'squash.json', {'method': 'delete'} )
    
    projects = client.get( '*.json' )
    assert_equal( len(projects), 0 )

def teardown():
    os.system('rm -rf .primary 2>/dev/null')

tests = [
    test_get_projects,
    test_put_project,
    test_get_project,
    test_post_project,
    test_delete_project,
]