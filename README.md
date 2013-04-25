RavenPy
=======

A python client for RavenDB

To run tests install nose:

    pip install nose

The library also uses requests:

	pip install requests

With nose and requests installed

	python runtests.py


Usage:

Create a client like so:

	from ravenpy import client as rdb

	client = rdb('localhost', 'test', 8080)

Store a document:

	client.store({
        "title": "test document",
        "deleted": True,
        "type": "TestDoc"
    })

Delete a document:

 	client.delete(documentId)

Create an index:

	index = {
		'alias': 'doc',
		'where': 'doc.type=="TestDoc"',
		'select': 'new { doc.deleted }'
	}

    client.createIndex(index, 'documentsByState')

Query the index:

	results = client.query('documentsByState', {
		'deleted': True,
		'type': 'TestDoc'
	})

Delete the index:

	client.deleteIndex('documentsByTitle')