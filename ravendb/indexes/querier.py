import requests


class querier(object):

    def __init__(self, client, indexId):
        self._client = client
        self._indexId = indexId

    def query(self, query):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        parsedQuery = ''
        fetchPart = ''
        for key, value in query['query'].items():
            parsedQuery = '{1}:{2}&{0}'.format(parsedQuery, key, value)
        if 'fetch' in query.keys():
            for projection in query['fetch']:
                fetchPart = '{1}={2}&{0}'.format(fetchPart, 'fetch', projection)

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
