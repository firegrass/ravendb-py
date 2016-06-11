import json
import requests


class bulk(object):

    def __init__(self, client, transactions):
        self._client = client
        self._transactions = transactions

    def process(self):
        bulk = []

        for transaction in self._transactions:
            bulk.append({
                "Method": transaction["action"],
                "Document": transaction["doc"],
                "Key": transaction["id"],
                "Metadata": transaction["metadata"]
            })

        url = '{0}/databases/{1}/bulk_docs'.format(self._client.url, self._client.database)

        r = self._client._post(url, data=json.dumps(bulk))

        if r.status_code == 200:
            response = r.json()
        else:
            raise Exception(
                'Error processing bulk Http :{0}'.format(
                    r.status_code
                ), r.text
            )
