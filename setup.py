#!/usr/bin/env python

import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

install_requires = [x for x in open(os.path.join(here, 'requirements.txt')).read().split('\n') if len(x) > 0]
testing_extras = [x for x in open(os.path.join(here, 'test_requirements.txt')).read().split('\n')
                  if len(x) > 0 and not x.startswith('-')]

setup(
    name='ndnkdf',
    version='0.3',
    description='Fast PBKDF2-HMAC-SHA512 using Nettle',
    long_description=README,
    author='Fredrik Thulin',
    author_email='fredrik@thulin.net',
    url='https://www.nordu.net/',
    license='BSD',
    packages=['ndnkdf',],
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=install_requires,
    extras_require={'testing': testing_extras,},
)
