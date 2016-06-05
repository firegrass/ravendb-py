import json
import requests
from ravendb.support import buncher as b


class querier(object):

    def __init__(self, client, indexId):
        self._client = client
        self._indexId = indexId

    def query(self, query = '', options = {}):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        genQuery = ''

        if not isinstance(query, basestring):
            parsedQuery = ''
            for key, value in query.items():
                genQuery = '{0} AND {1}:{2}'.format(parsedQuery, key, value)
            genQuery = parsedQuery[5:]
            options['query'] = genQuery
        else:
            options['query'] = query

        options['start'] = 0
        options['pageSize'] = 1024

        request = requests.get(
            '{0}/databases/{1}/indexes/{2}'.format(
                self._client.url,
                self._client.database,
                self._indexId,
            ),
            params=options,
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
