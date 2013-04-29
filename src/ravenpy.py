import json
import requests
import time
from config import config as cfg
from documents import storer as s
from documents import deleter as d
from documents import loader as l
from indexes import indexer as i
from indexes import querier as q


class client(object):

    def __init__(self, host, database, port):
        self.host = host
        self.database = database
        self.port = port
        self.url = 'http://{0}:{1}'.format(host, port)
        self.config = cfg()
        self.commands = commands()

    def configure(self, configuration):
        self.config = configuration

    def store(self, documents):
        return commands.store(documents)

    def update(self, updates):
        return commands.update(updates)

    def delete(self, documentIds):
        return commands.delete(documentIds)

    def createIndex(self, index, indexId):
        return command.createIndex(index, indexId)

    def deleteIndex(self, indexId):
        return command.deleteIndex(indexId)

    def load(self, documentIds):

        results = []

        for docId in documentIds:
            results.append(l.loader(self, docId).load())

        return results

    def query(self, indexId, query):
        querier = q.querier(self, indexId)
        response = querier.query(query)

        attempt = 0
        maxAttempts = self.config.maxAttemptsToWaitForNonStaleResults

        if self.config.waitForNonStaleResults:
            while response["IsStale"] is True:
                time.sleep(self.config.secondsToWaitForNonStaleResults)
                if attempt <= maxAttempts:
                    attempt = attempt + 1
                    response = querier.query(query)
                else:
                    return response

        return response


class commands(object):

    def __init__(self):
        pass

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

    def createIndex(self, index, indexId):
        return i.indexer(self, indexId).index(index)

    def deleteIndex(self, indexId):
        return i.indexer(self, indexId).delete()
