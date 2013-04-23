import json
import requests


class deleter(object):

    def __init__(self, client, documentId):
        self._client = client
        self._documentId = documentId

    def delete(self):
        headers = {"Content-Type": "application/json", "Accept": "text/plain"}
        request = requests.delete('{0}/databases/{1}/docs/{2}'.format(self._client.url, self._client.database, self._documentId), 
            headers=headers)

        if request.status_code == 204:
            return True
        else:
            raise Exception('Error deleting document Http :{0}'.format(request.status_code))