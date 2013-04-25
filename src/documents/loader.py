import json
import requests


class loader(object):

    def __init__(self, client, documentId):
        self._client = client
        self._documentId = documentId

    def load(self):
        headers = {"Content-Type": "application/json", "Accept": "text/plain"}
        request = requests.get(
            '{0}/databases/{1}/docs/{2}'.format(
                self._client.url, self._client.database, self._documentId
            ),
            headers=headers
        )

        if request.status_code == 200:
            return request.json()
        else:
            raise Exception(
                'Error getting document Http :{0}'.format(
                    request.status_code
                )
            )
