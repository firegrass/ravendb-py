import os
import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import yaml
import ravendb

CONFIG = yaml.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ravendb.conf')))

class TestCase(unittest.TestCase):

    def get_store(self):
        return ravendb.store(CONFIG['uri'], CONFIG['db'])

    def get_uri(self):
        return CONFIG['uri']

    def get_db(self):
        return CONFIG['db']
