import ravenpy
import unittest
from ravenpy import client as rdb


class test_when_using_ravenpy_client_for_indexes(unittest.TestCase):

    def setUp(self):
        self.client = rdb('localhost', 'test', 8080)
        pass

    def tearDown(self):
        pass

    def test_it_is_possible_to_create_a_new_index(self):

        index = {'Map': 'from doc in docs\r\nselect new { doc.title }'}
        indexId = None
        indexId = self.client.createIndex(index, 'documentsByTitle')

        self.assertEqual(indexId, 'documentsByTitle')
        self.client.deleteIndex('documentsByTitle')

    def test_it_is_possible_to_delete_an_index(self):

        index = {'Map': 'from doc in docs\r\nselect new { doc.title }'}
        indexId = None
        indexId = self.client.createIndex(index, 'documentsByTitle')

        result = self.client.deleteIndex('documentsByTitle')
        self.assertEqual(True, result)
