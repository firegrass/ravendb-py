import json
import requests


class indexer(object):

    def __init__(self, client, indexId):
        self._client = client
        self._indexId = indexId

    def index(self, index):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        request = requests.put('{0}/databases/{1}/indexes/{2}'.format(self._client.url, self._client.database, self._indexId), 
            data=json.dumps(index), headers=headers)

        if request.status_code == 201:
            response = request.json()
            if 'Index' in response:
                return response['Index']
            else:
                raise Exception('Creating index did not return the expected response')
        else:
            raise Exception('Error creating index Http :{0}{1}'.format(request.status_code)) 

    def delete(self):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        request = requests.delete('{0}/databases/{1}/indexes/{2}'.format(self._client.url, self._client.database, self._indexId), 
            headers=headers)

        if request.status_code == 204:
            return True
        else:
            raise Exception('Error deleting index Http :{0}{1}'.format(request.status_code))   