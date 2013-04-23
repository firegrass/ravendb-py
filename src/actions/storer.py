import json
import requests


class storer(object):

    def __init__(self, client, document):
        self._client = client
        self._document = document

    def store(self):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        request = requests.post('{0}/databases/{1}/docs'.format(self._client.url, self._client.database), 
            data=json.dumps(self._document), headers=headers)

        if request.status_code == 201:
            response = request.json()
            if 'Key' in response:
                return request.json()['Key']
            else:
                raise Exception('Storing document did not return the expected response')
        else:
            raise Exception('Error storing document Http :{0}'.format(request.status_code))  

    def update(self, documentId):
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        request = requests.put('{0}/databases/{1}/docs/{2}'.format(self._client.url, self._client.database, documentId), 
            data=json.dumps(self._document), headers=headers)

        if request.status_code == 201:
            response = request.json()
            if 'Key' in response:
                return request.json()['Key']
            else:
                raise Exception('Storing document did not return the expected response')
        else:
            raise Exception('Error storing document Http :{0}'.format(request.status_code))  