import ravenpy
import unittest
from ravenpy import client as rdb


class test_when_using_ravenpy_client_for_documents(unittest.TestCase):

    def setUp(self):
        self.client = rdb('localhost', 'test', 8080)
        pass

    def tearDown(self):
        pass

    def test_it_is_possible_to_store_a_new_document(self):

        documentId = None
        documentId = self.client.store({
            "title": "test document"
        })

        self.assertNotEqual(documentId, None)
        self.client.delete(documentId)

    def test_it_is_possible_to_delete_a_document(self):

        documentId = None
        documentId = self.client.store({
            "title": "test document"
        })

        result = None
        result = self.client.delete(documentId)

        self.assertEqual(result, True)

    def test_it_is_possible_to_load_an_existing_document(self):

        documentId = None
        documentId = self.client.store({
            "title": "test document"    
        })

        result = None
        result = self.client.load(documentId)

        containsKey = "title" in result

        self.assertEqual("test document", result["title"])
        self.client.delete(documentId)

    def test_it_is_possible_to_update_an_existing_document(self):

        documentId = None
        documentId = self.client.store({
            "title": "test document"    
        })

        result = None
        result = self.client.load(documentId)

        if("title" in result):
            result["title"] = "test document update"

        self.client.update(result, documentId)

        result = None
        result = self.client.load(documentId)

        if("title" in result):
            result["title"] = "test document update"

        self.assertEqual("test document update", result["title"])
        self.client.delete(documentId)
