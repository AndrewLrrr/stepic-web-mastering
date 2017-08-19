#!/usr/bin/python3


def app(environ, start_response):
    query = '\n'.join(environ.get('QUERY_STRING', '').strip().split('&'))
    start_response('200 OK', [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(query)))
    ])
    return [query.encode('utf-8')]
