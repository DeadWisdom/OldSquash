#-*- coding:utf-8 -*-
#
# Copyright (C) 2009 - Brantley Harris <brantley.harris@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt

import os
from setuptools import setup, find_packages

def read(file):
    return open(os.path.join(os.path.dirname(__file__), file)).read()

setup(name='squash',
      version = 'dev',
      description = 'A distributed, highly configurable issue tracking system.',
      long_description = read('ABOUT.txt'),
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Bug Tracking',
      ],
      keywords = 'bug tracker issue tracking project management',
      author = 'Brantley Harris',
      author_email = 'deadwisdom@gmail.com',
      url = 'http://www.bitbucket.org/DeadWisdom/squash/',
      license = 'BSD',
      packages = find_packages(exclude=['docs', 'design', 'tests']),
      package_data = {
        'squash': ['media/*.css', 'media/icons/*.png', 'js/*.js', 'js/*/*.js'],
      },
      zip_safe = False,
      install_requires = [
        'sqlalchemy',
        'pyyaml',
        'argparse',
      ],
      extras_require = {
        'sqlite': ["sqlite3>=2.0"],
      },
      entry_points = {
        'console_scripts': [
          'squash = squash.command:run',
        ],
      })