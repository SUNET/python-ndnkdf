#!/usr/bin/env python

from distutils.core import setup
from setuptools import setup, find_packages

setup(name		= 'ndnkdf',
      version		= '0.1',
      description	= 'Fast PBKDF2-HMAC-SHA512 using Nettle',
      author		= 'Fredrik Thulin',
      author_email	= 'fredrik@thulin.net',
      url		= 'http://www.nordu.net/',
      license		= 'BSD',
      packages		= find_packages(),
      test_suite	= "ndnkdf.tests.suite",
      test_requires	= ['unittest2', 'pbkdf2'],
     )
