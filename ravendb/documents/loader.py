import json
import requests


class loader(object):

    def __init__(self, client):
        self._client = client

    def load(self, documentIds):
        request = requests.post(
            '{0}/databases/{1}/queries'.format(
                self._client.url, self._client.database
            ),
            data=json.dumps(documentIds),
            headers=self._client.defaultRequestHeaders
        )

        if request.status_code == 200:
            return request.json()["Results"]
        else:
            raise Exception(
                'Error getting document Http :{0}'.format(
                    request.status_code
                )
            )
