import requests
from six import string_types

class querier(object):

    def __init__(self, client, indexId):
        self._client = client
        self._indexId = indexId

    def query(self, query = '', fetch = {}):

        qs = {}
        genQuery = ''

        if not isinstance(query, string_types):
            parsedQuery = ''
            for key, value in query.items():
                genQuery = '{0} AND {1}:{2}'.format(parsedQuery, key, value)
            genQuery = parsedQuery[5:]
            qs['query'] = genQuery
        else:
            qs['query'] = query

        # HACK make configurable / paging?
        qs['start'] = 0
        qs['pageSize'] = 1024

        if len(fetch) > 0:
            qs['fetch'] = fetch

        queryUrl = '{0}/databases/{1}/indexes/{2}'.format(
                self._client.url,
                self._client.database,
                self._indexId
        )

        request = self._client._get(queryUrl, params=qs)

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
