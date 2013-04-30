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

        index = {
            'alias': 'doc',
            'where': 'doc.type=="TestDoc"',
            'select': 'new { doc.deleted }'
        }
        indexId = None
        indexId = self.client.createIndex(index, 'documentsByTitle')

        self.assertEqual(indexId, 'documentsByTitle')
        self.client.deleteIndex('documentsByTitle')

    def test_it_is_possible_to_delete_an_index(self):

        index = {
            'alias': 'doc',
            'where': 'doc.type=="TestDoc"',
            'select': 'new { doc.deleted }'
        }
        indexId = None
        indexId = self.client.createIndex(index, 'documentsByTitle')

        result = self.client.deleteIndex('documentsByTitle')
        self.assertEqual(True, result)

    def test_it_is_possible_to_query_an_index(self):

        docIds = self.client.store([{
            "title": "test document",
            "deleted": True,
            "type": "TestDoc"
        }, {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        }, {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        }])

        index = {
            'alias': 'doc',
            'where': 'doc.type=="TestDoc"',
            'select': 'new { doc.deleted }'
        }

        self.client.createIndex(index, 'documentsByState')
        query = self.client.query('documentsByState', {'deleted': False})

        self.client.delete(docIds)
        self.client.deleteIndex('documentsByTitle')

        self.assertEqual(len(query.Results), 2)

    def test_it_is_possible_to_query_an_index_with_multiple_arguments(self):

        docIds = self.client.store([{
            "title": "test document",
            "deleted": True,
            "type": "DocType"
        }, {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        }, {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        }])

        index = {
            'alias': 'doc',
            'select': 'new { doc.deleted, doc.type }'
        }

        self.client.createIndex(index, 'documentsByState')
        query = self.client.query('documentsByState', {
            'deleted': True,
            'type': 'DocType'
        })

        self.client.delete(docIds)
        self.client.deleteIndex('documentsByTitle')

        self.assertEqual(len(query.Results), 1)
