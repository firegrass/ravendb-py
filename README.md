ravendb-py
=======

[![Build Status](https://travis-ci.org/firegrass/ravendb-py.svg?branch=master)](https://travis-ci.org/firegrass/ravendb-py)

A python client for RavenDB

Usage:

Create a document store like so:

	import ravendb

	client = ravendb.store(url='http://localhost:8080', database='test')

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

	results = session.load(list_of_documentIds)


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

	# single query argument
	results = session.query('documentsByState', { 'query': {
		        'deleted': True
		    }
	})

	# multiple arguments

	results = session.query('documentsByState', { 'query': {
		        'deleted': True,
		        'type': "TestDoc"

		    }
	})

	# Usage of projections (fetches) to only fetch particular data
	results = session.query('documentsByState', { 'query': {
		        'deleted': True,
		        'type': "TestDoc"

		    },
		    'fetch' : ['title', 'type']
	})



Delete the index:

	session.deleteIndex('documentsByTitle')

To run tests install nose:

    pip install nose

The library also uses requests:

	pip install requests

With nose and requests installed

	python runtests.py
