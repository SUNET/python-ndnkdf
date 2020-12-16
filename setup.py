#!/usr/bin/env python

import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

install_requires = [
    'pbkdf2',
]

testing_extras = [
    'coverage==3.6',
    'pbkdf2',
]

setup(
    name='ndnkdf',
    version='0.2',
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
