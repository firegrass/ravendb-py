import json
import requests
from ravendb.support import buncher as b


class querier(object):

    def __init__(self, client, indexId):
        self._client = client
        self._indexId = indexId

    def query(self, query):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        parsedQuery = ''

        for key, value in query.items():
            parsedQuery = '{1}:{2}&{0}'.format(parsedQuery, key, value)

        request = requests.get(
            '{0}/databases/{1}/indexes/{2}?query={3}'.format(
                self._client.url,
                self._client.database,
                self._indexId,
                parsedQuery
            ),
            headers=headers
        )

        if request.status_code == 200:
            response = request.json()

            if 'TotalResults' in response:
                results = b.buncher({
                    "IsStale": response["IsStale"],
                    "documents": []}
                ).bunch()

                for value in response["Results"]:
                    results.documents.append(
                        b.buncher(value).bunch()
                    )

                return results

            else:
                raise Exception(
                    'Query response unexpected Http: {0}'.format(
                        request.status_code
                    )
                )
        else:
            raise Exception(
                'Error querying index Http :{0}'.format(
                    request.status_code
                )
            )
