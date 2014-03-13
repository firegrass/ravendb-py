RavenPy
=======

A python client for RavenDB

Usage:

Create a document store like so:

	from ravendb

	client = store(url='http://localhost:8080', db='test')

Open a session:

	session = client.createSession()

Store documents:

	session.store([{
        "title": "test document",
        "deleted": True,
        "type": "TestDoc"
    }])

	session.save()

Load documents:

	results = session.load(documentIds)

Update documents:

    doc = results[0]
    docId = documentIds[0]

    doc.title = "test document update"

    session.update([{
        "id": docId,
        "doc": doc
    }])

    session.save()

Delete documents:

 	session.delete(documentIds)
 	session.save()

Create an index:

	index = {
		'alias': 'doc',
		'where': 'doc.type=="TestDoc"',
		'select': 'new { doc.deleted }'
	}

    session.createIndex(index, 'documentsByState')

Query the index:

	results = session.query('documentsByState', {
		'deleted': True
	})

Delete the index:

	session.deleteIndex('documentsByTitle')

To run tests install nose:

    pip install nose

The library also uses requests and bunch:

	pip install requests
	pip install bunch

With nose and requests installed

	python runtests.py
