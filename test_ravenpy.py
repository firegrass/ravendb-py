from ravenpy import client as rdb
import unittest


class test_ravenpy(unittest.TestCase):

    def test_post(self):

        client = rdb('localhost', 'test', 8080)

        result = client.insert({
            "title": "test document"
        })

        self.assertEqual(result, 201)
