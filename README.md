ravendb-py
=======

[![Build Status](https://travis-ci.org/firegrass/ravendb-py.svg?branch=master)](https://travis-ci.org/firegrass/ravendb-py)

A python client for RavenDB

Usage:

Create a document store like so:

	import ravendb

	c1 = ravendb.store(url='http://localhost:8080', database='test')
	c2 = ravendb.store(url='http://localhost:8080', database='test2', 
	                   apikey='e49eb756-39b3-48c6-a301-76c33ef936bf')

Open a session:

	session = client.createSession()

Store documents:

	session.store([{
            "title": "test document",
            "deleted": True,
            "type": "TestDoc",
            "@metadata": { "Raven-Entity-Name": "Test" }
        }])
    
    	session.store([session.createDocument('Test', {
            "title": "test document",
            "deleted": True,
            "type": "TestDoc"
        }]))

	session.save()

Load documents:

	results = session.load(['Test/1', 'Test/2', 'Test/3'])


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

 	session.delete(['Test/1', 'Test/2', 'Test/3'])
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
	results = session.query('documentsByState', 'query'={'deleted': True })

	# multiple arguments
	results = session.query('documentsByState', 'query'={
		        'deleted': True,
		        'type': "TestDoc"
		    }
	)

	# Usage of projections (fetches) to only fetch particular data
	results = session.query('documentsByState', 'query'={
		        'deleted': True,
		        'type': "TestDoc"
		    },
		    'fetch' : ['title', 'type']
	)

Delete the index:

	session.deleteIndex('documentsByTitle')

To run tests install nose:

    pip install nose
    nosetests

The library also uses requests:

	pip install -r requirements.txt

