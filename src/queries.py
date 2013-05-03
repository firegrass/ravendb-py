import time
from documents import loader as l
from documents import bulkloader as bl
from indexes import querier as q

class queries(object):

    def __init__(self, client):
        self._client = client

    def load(self, documentIds):

        results = []

        for docId in documentIds:
            results.append(l.loader(self._client, docId).load())

        return results

    def bulkLoad(self, documentIds):

        return bl.bulkloader(self._client, documentIds).load()

    def query(self, indexId, query):
        querier = q.querier(self._client, indexId)
        response = querier.query(query)

        attempt = 0
        maxAttempts = self._client.config.maxAttemptsToWaitForNonStaleResults

        if self._client.config.waitForNonStaleResults:
            while response["IsStale"] is True:
                time.sleep(self._client.config.secondsToWaitForNonStaleResults)
                if attempt <= maxAttempts:
                    attempt = attempt + 1
                    response = querier.query(query)
                else:
                    return response

        return response
