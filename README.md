RavenPy
=======

A python client for RavenDB

Usage:

Create a document store like so:

	from ravenpy import store as store

	client = store('http://localhost:8080', 'test')

Open a session:

	session = client.createSession()

Store documents:

	client.store([{
        "title": "test document",
        "deleted": True,
        "type": "TestDoc"
    }])

Load documents:

	results = client.load(documentIds)

Update documents:

    doc = results[0]
    docId = documentIds[0]

    doc.title = "test document update"

    client.update([{
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

The library also uses requests and bunch:

	pip install requests
	pip install bunch

With nose and requests installed

	python runtests.py
