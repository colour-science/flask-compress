import gzip
import StringIO

from flask import request


class Gzip(object):
    def __init__(self, app, compress_level=6, minimum_size=500):
        self.app = app
        self.compress_level = compress_level
        self.minimum_size = minimum_size
        self.mimetypes = ['text/html', 'text/css', 'text/xml',
                          'application/json', 'application/javascript']
        self.app.after_request(self.after_request)

    def after_request(self, response):
        accept_encoding = request.headers.get('Accept-Encoding', '')

        if 'gzip' not in accept_encoding.lower():
            return response

        if response.mimetype not in self.mimetypes:
            return response
        else:
            response.direct_passthrough = False

        if (response.status_code not in xrange(200, 300) or
            len(response.data) < self.minimum_size or
            'Content-Encoding' in response.headers):
            return response

        gzip_buffer = StringIO.StringIO()
        gzip_file = gzip.GzipFile(mode='wb', compresslevel=self.compress_level,
                                  fileobj=gzip_buffer)
        gzip_file.write(response.data)
        gzip_file.close()

        response.data = gzip_buffer.getvalue()
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = len(response.data)

        return response
