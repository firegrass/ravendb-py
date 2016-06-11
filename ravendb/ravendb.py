from .config import config as cfg
from .commands import commands as commands
from .queries import queries as queries
from .support import idgenerator as idgenerator
from .documents import cache as c
import requests

class store(object):

    def __init__(self, url='http://localhost:8080', database='test', apiKey=None,
                 waitForNonStaleResults=False,
                 secondsToWaitForNonStaleResults=0.5,
                 maxAttemptsToWaitForNonStaleResults=10):
        self.database = database
        self.url = url
        self.config = cfg()
        self.config.apiKey = apiKey
        self.config.waitForNonStaleResults = waitForNonStaleResults
        self.config.secondsToWaitForNonStaleResults = secondsToWaitForNonStaleResults
        self.config.maxAttemptsToWaitForNonStaleResults = maxAttemptsToWaitForNonStaleResults

    def createSession(self):
        return session(self.url, self.database, self.config)


class session(object):

    def __init__(self, url, database, config):
        self.url = url
        self.database = database
        self.config = config
        self.commands = commands(self)
        self.queries = queries(self)
        self._cache = c.cache(idgenerator.hilo(self))
        self.defaultRequestHeaders = { "Content-Type": "application/json", "Accept": "text/plain" }

    def updateAuthorizationFromApiKey(self):
        if self.config.apiKey is None:
            return

        auth_check_url = '{0}/databases/{1}'.format(self.url, self.database)
        res = requests.get(auth_check_url, headers=self.defaultRequestHeaders)
        if res.status_code != 401:
            return

        if 'OAuth-Source' not in res.headers:
            raise Exception('OAuth-Source not in headers')

        oauth_url = res.headers['OAuth-Source']
        headers = {
            'api-key': self.config.apiKey,
            'accept': 'application/json;charset=UTF-8',
            'grant_type': 'client_credentials'
        }
        res = requests.get(oauth_url, headers=headers)
        if res.status_code == 200:
            self.defaultRequestHeaders['Authorization'] = 'Bearer ' + res.text

    def _mergeHeaders(self, headers = {}):
        h = self.defaultRequestHeaders
        for header in headers:
            h[header] = headers[header]
        return h

    def _get(self, queryUrl, params = {}, headers = {}):
        headers = self._mergeHeaders(headers)
        res = requests.get(queryUrl, params=params, headers=headers)
        if res.status_code != 401:
            return res
        self.updateAuthorizationFromApiKey()
        return requests.get(queryUrl, params=params, headers=headers)

    def _post(self, queryUrl, data, headers = {}):
        headers = self._mergeHeaders(headers)
        res = requests.post(queryUrl, data=data, headers=headers)
        if res.status_code != 401:
            return res
        self.updateAuthorizationFromApiKey()
        return requests.post(queryUrl, data=data, headers=headers)

    def _put(self, queryUrl, data, headers = {}):
        headers = self._mergeHeaders(headers)
        res = requests.put(queryUrl, data=data, headers=headers)
        if res.status_code != 401:
            return res
        self.updateAuthorizationFromApiKey()
        return requests.put(queryUrl, data=data, headers=headers)

    def _delete(self, queryUrl, headers = {}):
        headers = self._mergeHeaders(headers)
        res = requests.delete(queryUrl, headers=headers)
        if res.status_code != 401:
            return res
        self.updateAuthorizationFromApiKey()
        return requests.post(queryUrl, headers=headers)

# Shouldn't be changing a session configuration, create a new one
#    def configure(self, configuration):
#        self.config = configuration

    def save(self):
        self.commands.bulk(self._cache.list())
        self._cache.reset()

    def store(self, documents):
        return self._cache.add(documents)

    def update(self, updates):
        return self._cache.update(updates)

    def delete(self, documentIds):
        self._cache.delete(documentIds)

    def createIndex(self, index, indexId):
        return self.commands.createIndex(index, indexId)

    def deleteIndex(self, indexId):
        return self.commands.deleteIndex(indexId)

    def load(self, documentIds):
        return self.queries.load(documentIds)

    def query(self, indexId, query, fetch = {}):
        return self.queries.query(indexId, query, fetch)

    def createDocument(self, entityType, doc = {}):
        if '@metadata' not in doc:
            doc['@metadata'] = {}
        doc['@metadata']['Raven-Entity-Name'] = entityType
        return doc
