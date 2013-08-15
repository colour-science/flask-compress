import gzip
import StringIO

from flask import request


class Compress(object):
    """
    The Compress object allows your application to use Flask-Compress.

    When initialising a Compress object you may optionally provide your
    :class:`flask.Flask` application object if it is ready. Otherwise,
    you may provide it later by using the :meth:`init_app` method.

    :param app: optional :class:`flask.Flask` application object
    :type app: :class:`flask.Flask` or None
    """
    def __init__(self, app=None):
        """
        An alternative way to pass your :class:`flask.Flask` application
        object to Flask-Compress. :meth:`init_app` also takes care of some
        default `settings`_.

        :param app: the :class:`flask.Flask` application object.
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        defaults = [
            ('COMPRESS_MIMETYPES', ['text/html', 'text/css', 'text/xml',
                                'application/json', 'application/javascript']),
            ('COMPRESS_DEBUG', False),
            ('COMPRESS_LEVEL', 6),
            ('COMPRESS_MIN_SIZE', 500)
        ]

        for k, v in defaults:
            app.config.setdefault(k, v)

        if app.config['COMPRESS_MIMETYPES']:
            self.app.after_request(self.after_request)

    def after_request(self, response):
        if self.app.debug and not self.app.config['COMPRESS_DEBUG']:
            return response

        accept_encoding = request.headers.get('Accept-Encoding', '')

        if 'gzip' not in accept_encoding.lower():
            return response

        if response.mimetype not in self.app.config['COMPRESS_MIMETYPES']:
            return response

        response.direct_passthrough = False

        if (response.status_code not in xrange(200, 300) or
            len(response.data) < self.app.config['COMPRESS_MIN_SIZE'] or
            'Content-Encoding' in response.headers):
            return response

        level = self.app.config['COMPRESS_LEVEL']

        gzip_buffer = StringIO.StringIO()
        gzip_file = gzip.GzipFile(mode='wb', compresslevel=level,
                                  fileobj=gzip_buffer)
        gzip_file.write(response.data)
        gzip_file.close()

        response.data = gzip_buffer.getvalue()
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Vary'] = 'Accept-Encoding'
        response.headers['Content-Length'] = len(response.data)

        return response
