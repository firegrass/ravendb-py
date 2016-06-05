import json
import requests
import sys


class bulk(object):

    def __init__(self, client, transactions):
        self._client = client
        self._transactions = transactions

    def process(self):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        bulk = []

        for transaction in self._transactions:
            bulk.append({
                "Method": transaction["action"],
                "Document": transaction["doc"],
                "Key": transaction["id"],
                "Metadata": transaction["metadata"]
            })

        request = requests.post(
            '{0}/databases/{1}/bulk_docs'.format(
                self._client.url, self._client.database
            ),
            data=json.dumps(bulk), headers=headers
        )

        if request.status_code == 200:
            response = request.json()
        else:
            raise Exception(
                'Error processing bulk Http :{0}'.format(
                    request.status_code
                )
            )
