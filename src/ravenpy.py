import json
import requests
import time
from config import config as cfg
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
        self.config = cfg()

    def configure(self, configuration):
        self.config = configuration

    def store(self, documents):
        documentIds = []

        for item in documents:
            documentIds.append(s.storer(self, item).store())

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
                s.storer(self, update["doc"]).update(update["id"])
            )

        return documentIds

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
        indexer = i.indexer(self, indexId)
        response = indexer.query(query)

        attempt = 0
        maxAttempts = self.config.maxAttemptsToWaitForNonStaleResults

        if self.config.waitForNonStaleResults:
            while response["IsStale"] is True:
                time.sleep(self.config.secondsToWaitForNonStaleResults)
                if attempt <= maxAttempts:
                    attempt = attempt + 1
                    response = indexer.query(query)
                else:
                    return response

        return response
