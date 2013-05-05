from documents import storer as s
from documents import deleter as d
from documents import loader as l
from documents import bulk as b
from indexes import indexer as i


class commands(object):

    def __init__(self, client):
        self._client = client

    def bulk(self, transactions):
        b.bulk(self._client, transactions).process()

    def store(self, documents):
        documentIds = []

        for item in documents:
            documentIds.append(s.storer(self._client, item).store())

        return documentIds

    def update(self, updates):

        documentIds = []
        for update in updates:
            hasKey = 'doc', 'id' in update
            if not hasKey:
                raise Exception(
                    'Update requires a document and an id'
                )
            documentIds.append(
                s.storer(self._client, update["doc"]).update(update["id"])
            )

        return documentIds

    def delete(self, documentIds):

        deleted = False

        for docId in documentIds:
            deleted = d.deleter(self._client, docId).delete()

        return deleted

    def createIndex(self, index, indexId):
        return i.indexer(self._client, indexId).index(index)

    def deleteIndex(self, indexId):
        return i.indexer(self._client, indexId).delete()
