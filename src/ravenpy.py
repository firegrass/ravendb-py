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

    def store(self, document):
        return s.storer(self, document).store()

    def update(self, document, documentId):
        return s.storer(self, document).update(documentId)

    def delete(self, documentId):
        return d.deleter(self, documentId).delete()

    def load(self, documentId):
        return l.loader(self, documentId).load()

    def createIndex(self, index, indexId):
        return i.indexer(self, indexId).index(index)

    def deleteIndex(self, indexId):
        return i.indexer(self, indexId).delete()

    def query(self, indexId, query):
        return i.indexer(self, indexId).query(query)
