class cache(object):

    def __init__(self, idgenerator):
        self._cache = []
        self._idgenerator = idgenerator

    def reset(self):
        self._cache = []

    def list(self):
        return self._cache

    def add(self, documents):

        ids = []

        for document in documents:
            if '@metadata' not in document and 'Raven-Entity-Name' not in document['@metadata']:
                raise Exception('documents must have entity name')
            id = str(self._idgenerator.Create(document['@metadata']['Raven-Entity-Name']))
            ids.append(id)
            self._cache.append({
                "action": "PUT",
                "id": id,
                "doc": document,
                "metadata": document['@metadata']
            })

        return ids

    def delete(self, documentIds):

        for docId in documentIds:
            for index, item in enumerate(self._cache):
                if docId in item:
                    self._cache.remove(index)
            self._cache.append({
                "action": "DELETE",
                "id": docId,
                "doc": {},
                "metadata": {}
            })

    def update(self, documents):

        ids = []

        for update in documents:
            ids.append(update["id"])

            for index, item in enumerate(self._cache):
                if update["id"] in item:
                    self._cache[index]["doc"] = update["doc"]

        return ids
