import json
import http.client


class client(object):

    def __init__(self, host, database, port):
        self._host = host
        self._database = database
        self._port = port

    def insert(self, document):
        connection = http.client.HTTPConnection(self._host, self._port)
        connection.connect()

        connection.request
        (
            'POST',
            '/databases/{0}/docs'.format(self._database),
            json.dumps(document),
            {"Content-Type": "application/json"}
        )

        result = connection.getresponse()
        return result.status
