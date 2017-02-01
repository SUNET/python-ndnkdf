#!/usr/bin/env python

from setuptools import setup, find_packages
import sys, os

README = open(os.path.join(here, 'README.txt')).read()

testing_extras = [
    'nose==1.2.1',
    'nosexcover==1.0.8',
    'coverage==3.6',
    'unittest2',
    'pbkdf2',
]

setup(name		= 'ndnkdf',
      version		= '0.2',
      description	= 'Fast PBKDF2-HMAC-SHA512 using Nettle',
      author		= 'Fredrik Thulin',
      author_email	= 'fredrik@thulin.net',
      url		= 'https://www.nordu.net/',
      license		= 'BSD',
      packages		= find_packages(),
      test_suite	= "ndnkdf.tests.suite",
      zip_safe		= False,
      extras_require={
        'testing': testing_extras,
        },
     )
