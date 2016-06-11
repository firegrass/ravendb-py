#!/usr/bin/env python

from setuptools import setup, find_packages
import os
import platform


# Conditional include unittest2 for versions of python < 2.7
tests_require = ['nose', 'pyyaml']
platform_version = list(platform.python_version_tuple())[0:2]
if platform_version[0] != '3' and platform_version != ['2', '7']:
    tests_require.append('unittest2')

long_description = ('ravendb is a pure-Python implementation of for talking to RavenDB')

setup(
    name='ravendb',
    version='0.1',
    description='Python RavenDB client',
    long_description=long_description,
    author='Mark Woodhall',
    author_email='mark.woodhall@gmail.com',
    url='https://github.com/firegrass/ravendb-py',
    platforms='any',
    packages=['ravendb', 'ravendb.documents', 'ravendb.indexes', 'ravendb.support'],
    install_requires = [
        'requests>=2.2.1',
        'bunch>=1.0.1'
    ],
    test_suite='nose.collector',
    download_url = 'https://github.com/firegrass/ravendb-py/archive/e5d6f123f71ca59c0995225956e6dc32df50d26f.zip',
    keywords = "ravendb raven database",
    zip_safe=True
)
