import os
import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import yaml
from ravenpy import store as store

CONFIG = yaml.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ravendb.conf')))

class TestCase(unittest.TestCase):

    def get_store(self):
        return store(CONFIG['uri'], CONFIG['db'])
