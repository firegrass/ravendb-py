import ravenpy
import unittest
import test_base
from ravenpy import store as store


class test_when_using_ravenpy_session_for_indexes(test_base.TestCase):

    def setUp(self):
        self.session = self.get_store().createSession()
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
        indexId = self.session.createIndex(index, 'documentsByTitle')

        self.assertEqual(indexId, 'documentsByTitle')
        self.session.deleteIndex('documentsByTitle')

    def test_it_is_possible_to_delete_an_index(self):

        index = {
            'alias': 'doc',
            'where': 'doc.type=="TestDoc"',
            'select': 'new { doc.deleted }'
        }
        indexId = None
        indexId = self.session.createIndex(index, 'documentsByTitle')

        result = self.session.deleteIndex('documentsByTitle')
        self.assertEqual(True, result)

    def test_it_is_possible_to_query_an_index(self):

        docIds = self.session.store([{
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

        self.session.save()

        index = {
            'alias': 'doc',
            'where': 'doc.type=="TestDoc"',
            'select': 'new { doc.deleted }'
        }

        self.session.createIndex(index, 'documentsByState')
        query = self.session.query('documentsByState', {'deleted': False})

        self.session.delete(docIds)
        self.session.save()
        self.session.deleteIndex('documentsByTitle')
        self.assertEqual(query.documents[0].title, 'test document')
        self.assertEqual(query.documents[1].title, 'test document')

    def test_it_is_possible_to_query_an_index_with_multiple_arguments(self):

        docIds = self.session.store([{
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

        self.session.save()

        index = {
            'alias': 'doc',
            'select': 'new { doc.deleted, doc.type }'
        }

        self.session.createIndex(index, 'documentsByState')
        query = self.session.query('documentsByState', {
            'deleted': True,
            'type': 'DocType'
        })

        self.session.delete(docIds)
        self.session.save()
        self.session.deleteIndex('documentsByTitle')

        self.assertEqual(query.documents[0].title, 'test document')
