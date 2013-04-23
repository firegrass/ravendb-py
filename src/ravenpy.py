import json
import requests
from actions import storer as s
from actions import deleter as d
from actions import loader as l

class client(object):

    def __init__(self, host, database, port):
        self.host = host
        self.database = database
        self.port = port
        self.url = 'http://{0}:{1}'.format(host, port)


    def store(self, document):
        return s.storer(self, document).store()

    def update(self, document, documentId):
    	return s.storer(self, document).update(documentId)

    def delete(self, documentId):
        return d.deleter(self, documentId).delete()

    def load(self, documentId):
    	return l.loader(self, documentId).load()
