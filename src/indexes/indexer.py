import json
import requests


class indexer(object):

    def __init__(self, client, indexId):
        self._client = client
        self._indexId = indexId

    def index(self, index):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        request = requests.put(
            '{0}/databases/{1}/indexes/{2}'.format(
                self._client.url, self._client.database, self._indexId
            ),
            data=json.dumps(index), headers=headers)

        if request.status_code == 201:
            response = request.json()
            if 'Index' in response:
                return response['Index']
            else:
                raise Exception(
                    'Create index did not return the expected response'
                )
        else:
            raise Exception(
                'Error creating index Http :{0}{1}'.format(request.status_code)
            )

    def delete(self):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        request = requests.delete(
            '{0}/databases/{1}/indexes/{2}'.format(
                self._client.url, self._client.database, self._indexId
            ),
            headers=headers
        )

        if request.status_code == 204:
            return True
        else:
            raise Exception(
                'Error deleting index Http :{0}{1}'.format(request.status_code)
            )

    def query(self, query):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        parsedQuery = ''

        for key, value in query.items():
            parsedQuery = parsedQuery.join('{0}:{1}'.format(key, value))

        request = requests.get(
            '{0}/databases/{1}/indexes/{2}?query={3}'.format(
                self._client.url, self._client.database, self._indexId, parsedQuery
            ),
            headers=headers
        )

        if request.status_code == 200:
            response = request.json()

            if 'TotalResults' in response:
                while response["IsStale"] is True:
                    response = self.query(query)

                return response
            else:
                raise Exception(
                    'Query response unexpected Http: {0}'.format(
                        request.status_code
                    )
                )
        else:
            raise Exception(
                'Error querying index Http :{0}{1}'.format(
                    request.status_code
                )
            )
