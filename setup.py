#!/usr/bin/env python

from setuptools import setup, find_packages
import os
import platform


# Conditional include unittest2 for versions of python < 2.7
tests_require = ['nose', 'pyyaml']
platform_version = list(platform.python_version_tuple())[0:2]
if platform_version[0] != '3' and platform_version != ['2', '7']:
    tests_require.append('unittest2')

long_description = ('RavenPy is a pure-Python implementation of for talking to RavenDB')

setup(
    name='RavenPy',
    version='0.1',
    description='Python RavenDB client',
    long_description=long_description,
    author='Mark Woodhall',
    author_email='mark.woodhall@gmail.com',
    url='https://github.com/firegrass/RavenPy',
    platforms='any',
    packages=['RavenPy'],
    install_requires = [
        'requests>=2.2.1',
        'bunch>=1.0.1'
    ],
    test_suite='nose.collector',
    keywords = "ravendb raven database",
    zip_safe=True
)
