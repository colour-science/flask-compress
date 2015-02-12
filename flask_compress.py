import sys
from gzip import GzipFile
from io import BytesIO as IO

from flask import request, current_app


if sys.version_info[:2] == (2, 6):
    class GzipFile(GzipFile):
        """ Backport of context manager support for python 2.6"""
        def __enter__(self):
            if self.fileobj is None:
                raise ValueError("I/O operation on closed GzipFile object")
            return self

        def __exit__(self, *args):
            self.close()


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
                                    'application/json',
                                    'application/javascript']),
            ('COMPRESS_LEVEL', 6),
            ('COMPRESS_MIN_SIZE', 500)
        ]

        for k, v in defaults:
            app.config.setdefault(k, v)

        if app.config['COMPRESS_MIMETYPES']:
            app.after_request(self.after_request)

    def after_request(self, response):
        if self.app:
            app = self.app
        else:
            app = current_app

        if app.debug:
            return response

        accept_encoding = request.headers.get('Accept-Encoding', '')

        if 'gzip' not in accept_encoding.lower():
            return response

        if response.mimetype not in app.config['COMPRESS_MIMETYPES']:
            return response

        response.direct_passthrough = False

        if (response.status_code < 200 or
            response.status_code >= 300 or
            response.content_length < app.config['COMPRESS_MIN_SIZE'] or
            'Content-Encoding' in response.headers):
            return response

        level = app.config['COMPRESS_LEVEL']

        gzip_buffer = IO()
        with GzipFile(mode='wb',
                      compresslevel=level,
                      fileobj=gzip_buffer) as gzip_file:
            gzip_file.write(response.data)

        response.data = gzip_buffer.getvalue()

        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = response.content_length

        vary = response.headers.get('Vary')
        if vary:
            if 'Accept-Encoding' not in vary:
                response.headers['Vary'] = vary + ', Accept-Encoding'
        else:
            response.headers['Vary'] = 'Accept-Encoding'

        return response
