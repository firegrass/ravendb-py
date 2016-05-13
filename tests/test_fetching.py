import ravendb


def main():
    client = ravendb.store(url='http://live-test.ravendb.net/', database='DJ')
    session = client.createSession()
    result = session.query('documentsByState', {
        'query': {
            'deleted': True,
            'type': 'DocType'
        },
        'fetch': ['title', 'deleted']
    })
    print(result['Results'])


if __name__ == "__main__":
        main()