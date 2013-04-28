RavenPy
=======

A python client for RavenDB

Usage:

Create a client like so:

	from ravenpy import client as rdb

	client = rdb('localhost', 'test', 8080)

Store documents:

	client.store([{
        "title": "test document",
        "deleted": True,
        "type": "TestDoc"
    }])

Load documents:

	results = self.client.load(documentIds)

Update documents:

    doc = results[0]
    docId = documentIds[0]

    doc["title"] = "test document update"

    self.client.update([{
        "id": docId,
        "doc": doc
    }])

Delete documents:

 	client.delete(documentIds)

Create an index:

	index = {
		'alias': 'doc',
		'where': 'doc.type=="TestDoc"',
		'select': 'new { doc.deleted }'
	}

    client.createIndex(index, 'documentsByState')

Query the index:

	results = client.query('documentsByState', {
		'deleted': True
	})

Delete the index:

	client.deleteIndex('documentsByTitle')

To run tests install nose:

    pip install nose

The library also uses requests:

	pip install requests

With nose and requests installed

	python runtests.py
