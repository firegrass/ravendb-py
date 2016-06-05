import json
import requests
from ravendb.support import buncher as b


class loader(object):

    def __init__(self, client):
        self._client = client

    def load(self, documentIds):
        headers = {"Content-Type": "application/json", "Accept": "text/plain"}
        request = requests.post(
            '{0}/databases/{1}/queries'.format(
                self._client.url, self._client.database
            ),
            data=json.dumps(documentIds),
            headers=headers
        )

        if request.status_code == 200:
            results = []

            for value in request.json()["Results"]:
                results.append(b.buncher(value).bunch())

            return results
        else:
            raise Exception(
                'Error getting document Http :{0}'.format(
                    request.status_code
                )
            )
