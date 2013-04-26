import ravenpy
import unittest
from ravenpy import client as rdb


class test_when_using_ravenpy_client_for_documents(unittest.TestCase):

    def setUp(self):
        self.client = rdb('localhost', 'test', 8080)
        pass

    def tearDown(self):
        pass

    def test_it_is_possible_to_store_documents(self):

        documentIds = None
        documentIds = self.client.store([{
            "title": "test document"
        }, {
            "title": "test document 2"
        }])

        self.assertNotEqual(documentIds[0], None)
        self.assertNotEqual(documentIds[1], None)
        self.client.delete(documentIds)

    def test_it_is_possible_to_delete_documents(self):

        documentIds = None
        documentIds = self.client.store([{
            "title": "test document"
        }, {
            "title": "test document 2"
        }])

        result = None
        result = self.client.delete(documentIds)

        self.assertEqual(result, True)

    def test_it_is_possible_to_load_documents(self):

        documentIds = None
        documentIds = self.client.store([{
            "title": "test document"
        }, {
            "title": "test document 2"
        }])

        results = None
        results = self.client.load(documentIds)

        self.assertEqual("test document", results[0]["title"])
        self.assertEqual("test document 2", results[1]["title"])

        self.client.delete(documentIds)

    def test_it_is_possible_to_update_documents(self):

        documentIds = None
        documentIds = self.client.store([{
            "title": "test document"
        }])

        results = None
        results = self.client.load(documentIds)

        doc = results[0]
        docId = documentIds[0]

        if("title" in doc):
            doc["title"] = "test document update"

        self.client.update([{
            "id": docId,
            "doc": doc
        }])

        results = None
        results = self.client.load(documentIds)

        if("title" in results[0]):
            results[0]["title"] = "test document update"

        self.assertEqual("test document update", results[0]["title"])
        self.client.delete(documentIds)
