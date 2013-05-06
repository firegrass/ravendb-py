import ravenpy
import unittest
from ravenpy import store as store
from config import config as cfg


class test_when_configuring_ravenpy_session(unittest.TestCase):

    def setUp(self):
        self.session = store('localhost', 'test', 8080).createSession()
        pass

    def tearDown(self):
        pass

    def test_configuring_wait_for_non_stale_results(self):
        config = cfg()
        config.waitForNonStaleResults = False
        self.session.configure(config)
        self.assertEqual(self.session.config.waitForNonStaleResults, False)

    def test_configuring_how_long_to_wait_for_non_stale_results(self):
        config = cfg()
        config.secondsToWaitForNonStaleResults = 0.5
        self.session.configure(config)
        self.assertEqual(
            self.session.config.secondsToWaitForNonStaleResults,
            0.5
        )

    def test_configuring_how_many_attempts_to_make_for_non_stale_results(self):
        config = cfg()
        config.maxAttemptsToWaitForNonStaleResults = 50
        self.session.configure(config)
        self.assertEqual(
            self.session.config.maxAttemptsToWaitForNonStaleResults,
            50
        )
