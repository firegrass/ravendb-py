import json
import requests
import time
from config import config as cfg
from commands import commands as commands
from queries import queries as queries


class client(object):

    def __init__(self, host, database, port):
        self.host = host
        self.database = database
        self.port = port
        self.url = 'http://{0}:{1}'.format(host, port)
        self.config = cfg()
        self.commands = commands(self)
        self.queries = queries(self)

    def configure(self, configuration):
        self.config = configuration

    def store(self, documents):
        return self.commands.store(documents)

    def update(self, updates):
        return self.commands.update(updates)

    def delete(self, documentIds):
        return self.commands.delete(documentIds)

    def createIndex(self, index, indexId):
        return self.commands.createIndex(index, indexId)

    def deleteIndex(self, indexId):
        return self.commands.deleteIndex(indexId)

    def load(self, documentIds):
        return self.queries.load(documentIds)

    def query(self, indexId, query):
        return self.queries.query(indexId, query)
