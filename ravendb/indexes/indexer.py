import json
import requests


class indexer(object):

    def __init__(self, client, indexId):
        self._client = client
        self._indexId = indexId

    def index(self, index):

        def mapIndex(index):
            mapper = 'from {0} in docs'.format(index["alias"])
            if 'where' in index:
                mapper = '{0} where {1} '.format(mapper, index["where"])
            mapper = '{0} select {1}'.format(mapper, index["select"])
            return mapper

        createIndex = { 'Map': mapIndex(index) }

        url = '{0}/databases/{1}/indexes/{2}'.format(
            self._client.url,
            self._client.database,
            self._indexId)

        r = self._client._put(url, data=json.dumps(createIndex))

        if r.status_code == 201:
            j = r.json()
            if 'Index' in j:
                return j['Index']
            else:
                raise Exception(
                    'Create index did not return the expected response'
                )
        else:
            raise Exception(
                'Error creating index Http :{0}'.format(r.status_code)
            )

    def delete(self):
        url = '{0}/databases/{1}/indexes/{2}'.format(
            self._client.url,
            self._client.database,
            self._indexId)

        r = self._client._delete(url)

        if r.status_code == 204:
            return True
        else:
            raise Exception(
                'Error deleting index Http :{0}'.format(r.status_code)
            )
