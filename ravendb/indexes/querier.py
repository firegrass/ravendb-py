import json
import requests
#from ravendb.support import buncher as b


class querier(object):

    def __init__(self, client, indexId):
        self._client = client
        self._indexId = indexId

    def query(self, query):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        parsedQuery = ''
        fetchPart = ''
        for key, value in query.items():
            if key == 'fetch':
                for entry in query['fetch']:
                    fetchPart = '{1}={2}&{0}'.format(fetchPart, 'fetch', entry)
            else:
                parsedQuery = '{1}:{2}&{0}'.format(parsedQuery, key, value)

        queryUrl = '{0}/databases/{1}/indexes/{2}?query={3}{4}'.format(
                self._client.url,
                self._client.database,
                self._indexId,
                parsedQuery,
                fetchPart
            )

        print("URL Being used: " + queryUrl)

        request = requests.get(
            queryUrl,
            headers=headers
        )

        if request.status_code == 200:
            response = request.json()

            if 'TotalResults' in response:
                """results = b.buncher({
                    "IsStale": response["IsStale"],
                    "documents": []}
                ).bunch()

                for value in response["Results"]:
                    results.documents.append(
                        b.buncher(value).bunch()
                    )

                return results
                """
                return response

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
