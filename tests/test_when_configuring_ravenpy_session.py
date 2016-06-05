import ravendb
import unittest
import test_base

class test_when_configuring_ravenpy_session(test_base.TestCase):

    def tearDown(self):
        pass

    def test_configuring_wait_for_non_stale_results(self):
        self.session = ravendb.store(self.get_uri(), self.get_db(), waitForNonStaleResults = False).createSession()
        self.assertEqual(self.session.config.waitForNonStaleResults, False)

    def test_configuring_how_long_to_wait_for_non_stale_results(self):
        self.session = ravendb.store(self.get_uri(), self.get_db(), secondsToWaitForNonStaleResults = 0.5).createSession()
        self.assertEqual(
            self.session.config.secondsToWaitForNonStaleResults,
            0.5
        )

    def test_configuring_how_many_attempts_to_make_for_non_stale_results(self):
        self.session = ravendb.store(self.get_uri(), self.get_db(), maxAttemptsToWaitForNonStaleResults = 50).createSession()
        self.assertEqual(
            self.session.config.maxAttemptsToWaitForNonStaleResults,
            50
        )
