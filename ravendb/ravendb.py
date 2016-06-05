from config import config as cfg
from commands import commands as commands
from queries import queries as queries
from support import idgenerator as idgenerator
from documents import cache as c


class store(object):

    def __init__(self, url='http://localhost:8080', database='test',
                 waitForNonStaleResults=False,
                 secondsToWaitForNonStaleResults=0.5,
                 maxAttemptsToWaitForNonStaleResults=10):
        self.database = database
        self.url = url
        self.config = cfg()
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
        self._cache = c.cache(idgenerator.guid())

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

    def query(self, indexId, query):
        return self.queries.query(indexId, query)
