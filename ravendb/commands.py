from .documents import bulk as b
from .indexes import indexer as i


class commands(object):

    def __init__(self, client):
        self._client = client

    def bulk(self, transactions):
        b.bulk(self._client, transactions).process()

    def createIndex(self, index, indexId):
        return i.indexer(self._client, indexId).index(index)

    def deleteIndex(self, indexId):
        return i.indexer(self._client, indexId).delete()
