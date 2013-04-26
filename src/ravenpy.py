import json
import requests
from documents import storer as s
from documents import deleter as d
from documents import loader as l
from indexes import indexer as i


class client(object):

    def __init__(self, host, database, port):
        self.host = host
        self.database = database
        self.port = port
        self.url = 'http://{0}:{1}'.format(host, port)

    def store(self, documents):
        documentIds = []

        for item in documents:
            documentIds.append(s.storer(self, item).store())

        return documentIds

    def update(self, document, documentId):
        return s.storer(self, document).update(documentId)

    def delete(self, documentIds):

        deleted = False

        for docId in documentIds:
            deleted = d.deleter(self, docId).delete()

        return deleted

    def load(self, documentIds):

        results = []

        for docId in documentIds:
            results.append(l.loader(self, docId).load())

        return results

    def createIndex(self, index, indexId):
        return i.indexer(self, indexId).index(index)

    def deleteIndex(self, indexId):
        return i.indexer(self, indexId).delete()

    def query(self, indexId, query):
        return i.indexer(self, indexId).query(query)
