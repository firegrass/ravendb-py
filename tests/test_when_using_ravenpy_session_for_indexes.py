import ravendb
import unittest
import test_base
from time import sleep

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

        docIds = self.session.store([
            self.session.createDocument('Test', {
            "title": "test document",
            "deleted": True,
            "type": "TestDoc"
        }), self.session.createDocument('Test', {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        }), self.session.createDocument('Test', {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        })])
        self.session.save()

        index = {
            'alias': 'doc',
            'where': 'doc.type=="TestDoc"',
            'select': 'new { doc.deleted }'
        }

        self.session.createIndex(index, 'documentsByTitle')
        sleep(0.3)
        query = self.session.query('documentsByTitle', {'query': {'deleted': False}})
        self.session.deleteIndex('documentsByTitle')
        self.session.delete(docIds)
        self.session.save()
        self.assertEqual(query['Results'][0]['title'], 'test document')
        self.assertEqual(query['Results'][1]['title'], 'test document')


    def test_it_is_possible_to_query_an_index_with_multiple_arguments(self):

        docIds = self.session.store([
            self.session.createDocument('Test', {
            "title": "test document",
            "deleted": True,
            "type": "TestDoc"
        }), self.session.createDocument('Test', {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        }), self.session.createDocument('Test', {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        })])
        self.session.save()

        index = {
            'alias': 'doc',
            'select': 'new { doc.deleted, doc.type }'
        }

        self.session.createIndex(index, 'documentsByTitle')

        sleep(0.3)
        query = self.session.query('documentsByTitle', {
            'query' : {
                'deleted': True,
                'type': 'DocType'
            }
        })

        self.session.deleteIndex('documentsByTitle')
        self.session.delete(docIds)
        self.session.save()
        self.assertEqual(query['Results'][0]['title'], 'test document')


    def test_it_is_possible_to_query_an_index_and_fetch(self):
        docIds = self.session.store([
            self.session.createDocument('Test', {
            "title": "test document",
            "deleted": True,
            "type": "TestDoc"
        }), self.session.createDocument('Test', {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        }), self.session.createDocument('Test', {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        })])
        self.session.save()

        index = {
            'alias': 'doc',
            'where': 'doc.type=="TestDoc"',
            'select': 'new { doc.deleted }'
        }

        self.session.createIndex(index, 'documentsByTitle')
        sleep(0.3)
        query = self.session.query('documentsByTitle', query={'deleted': False}, fetch=['title'])
        self.session.deleteIndex('documentsByTitle')
        self.session.delete(docIds)
        self.session.save()
        self.assertTrue('title' in query['Results'][0].keys())
        self.assertTrue('deleted' not in query['Results'][0].keys())
        self.assertTrue('type' not in query['Results'][0].keys())
        self.assertTrue('title' in query['Results'][1].keys())
        self.assertTrue('deleted' not in query['Results'][1].keys())
        self.assertTrue('type' not in query['Results'][1].keys())




    def test_it_is_possible_to_query_an_index_with_multiple_fetches(self):
        docIds = self.session.store([
            self.session.createDocument('Test', {
            "title": "test document",
            "deleted": True,
            "type": "TestDoc"
        }), self.session.createDocument('Test', {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        }), self.session.createDocument('Test', {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        })])
        self.session.save()

        index = {
            'alias': 'doc',
            'where': 'doc.type=="TestDoc"',
            'select': 'new { doc.deleted }'
        }

        self.session.createIndex(index, 'documentsByTitle')
        sleep(0.3)
        query = self.session.query('documentsByTitle',
                                   query={'deleted': False },
                                   fetch=['title', 'type']
        )
        self.session.deleteIndex('documentsByTitle')
        self.session.delete(docIds)
        self.session.save()
        self.assertTrue('title' in query['Results'][0].keys())
        self.assertTrue('deleted' not in query['Results'][0].keys())
        self.assertTrue('type' in query['Results'][0].keys())
        self.assertTrue('title' in query['Results'][1].keys())
        self.assertTrue('deleted' not in query['Results'][1].keys())
        self.assertTrue('type' in query['Results'][1].keys())

    def test_it_is_possible_to_query_an_index_with_multiple_arguments_and_multiple_fetches(self):
        docIds = self.session.store([
            self.session.createDocument('Test', {
            "title": "test document",
            "deleted": True,
            "type": "TestDoc"
        }), self.session.createDocument('Test', {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        }), self.session.createDocument('Test', {
            "title": "test document",
            "deleted": False,
            "type": "TestDoc"
        })])
        self.session.save()
        index = {
            'alias': 'doc',
            'where': 'doc.type=="TestDoc"',
            'select': 'new {  doc.deleted, doc.type }'
        }
        print(self.session.createIndex(index, 'documentsByTitle'))
        # without a sleep between index creation and querying, an error will be thrown.
        sleep(1)
        query = self.session.query('documentsByTitle', {
            'deleted': True,
            'type': 'TestDoc'
        }, ['title', 'type'] )
        self.session.deleteIndex('documentsByTitle')
        self.session.delete(docIds)
        self.session.save()
        self.assertTrue('title' in query['Results'][0].keys())
        self.assertTrue('deleted' not in query['Results'][0].keys())
        self.assertTrue('type' in query['Results'][0].keys())


