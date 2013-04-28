import ravenpy
import unittest
from ravenpy import client as rdb
from config import config as cfg


class test_when_using_ravenpy_configure(unittest.TestCase):

    def setUp(self):
        self.client = rdb('localhost', 'test', 8080)
        pass

    def tearDown(self):
        pass

    def test_configuring_wait_for_non_stale_results(self):
        config = cfg()
        config.waitForNonStaleResults = False
        self.client.configure(config)
        self.assertEqual(self.client.config.waitForNonStaleResults, False)

    def test_configuring_how_long_to_wait_for_non_stale_results(self):
        config = cfg()
        config.secondsToWaitForNonStaleResults = 0.5
        self.client.configure(config)
        self.assertEqual(self.client.config.secondsToWaitForNonStaleResults, 0.5)

    def test_configuring_how_many_attempts_to_make_for_non_stale_results(self):
        config = cfg()
        config.maxAttemptsToWaitForNonStaleResults = 50
        self.client.configure(config)
        self.assertEqual(self.client.config.maxAttemptsToWaitForNonStaleResults, 50)
