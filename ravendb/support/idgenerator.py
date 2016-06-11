import uuid
import requests
import json


class guid(object):

    def Create(self, entityType = None):
        return uuid.uuid1()

class hilo(object):

    def __init__(self, client):
        self._keySeparator = '/'
        self._capacity = 16
        self._path = 'Raven/Hilo'
        self._hilo = {}
        self._client = client
        self._hiloUrl = '{0}/databases/{1}/docs/{2}/'.format(self._client.url, self._client.database, self._path)

    def Create(self, entityType):
        hiloUrl = self._hiloUrl + entityType
        if entityType not in self._hilo:
            self._hilo[entityType] = {}
            serverMax = self._getHilo(entityType)
            if serverMax == -1:
                doc = { 'max': self._capacity, '@metadata': { 'etag': '00000000-0000-0000-000000000000' } }
                r = self._client._put(hiloUrl, data=json.dumps(doc))
                next = 1
                self._hilo[entityType]['max'] = self._capacity
            else:
                next = serverMax + 1
                serverMax = serverMax + self._capacity
                r = self._client._put(hiloUrl, data=json.dumps({ 'max': serverMax }))
                self._hilo[entityType]['max'] = serverMax
        else:
            next = self._hilo[entityType]['cur'] + 1
            max = self._hilo[entityType]['max']
            if next > max:
                serverMax = self._getHilo(entityType)
                next = serverMax + 1
                serverMax = serverMax + self._capacity
                r = self._client._put(hiloUrl, data=json.dumps({ 'max': serverMax }))
                self._hilo[entityType]['max'] = serverMax

        self._hilo[entityType]['cur'] = next
        return entityType + self._keySeparator + str(next)

    def _getHilo(self, entityType):
        r = self._client._get(self._hiloUrl + entityType)
        if r.status_code == 200:
            return r.json()['max']
        elif r.status_code == 404:
            return -1
        raise Exception('Could not fetch Hilo doc for ' + entityType)
