import gzip
import StringIO

from flask import request


class Gzip(object):
    """
    The Gzip object allows your application to use Flask-Gzip.

    When initialising a Gzip object you may optionally provide your
    :class:`flask.Flask` application object if it is ready. Otherwise,
    you may provide it later by using the :meth:`init_app` method.

    :param app: optional :class:`flask.Flask` application object
    :type app: :class:`flask.Flask` or None
    """
    def __init__(self, app=None):
        """
        An alternative way to pass your :class:`flask.Flask` application
        object to Flask-Gzip. :meth:`init_app` also takes care of some
        default `settings`_.

        :param app: the :class:`flask.Flask` application object.
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        defaults = [
            ('GZIP_MIMETYPES', ['text/html', 'text/css', 'text/xml',
                                'application/json', 'application/javascript']),
            ('GZIP_DEBUG', False),
            ('GZIP_LEVEL', 6),
            ('GZIP_MIN_SIZE', 500)
        ]

        for k, v in defaults:
            app.config.setdefault(k, v)

        if app.config['GZIP_MIMETYPES']:
            self.app.after_request(self.after_request)

    def after_request(self, response):
        if self.app.debug and not self.app.config['GZIP_DEBUG']:
            return response

        accept_encoding = request.headers.get('Accept-Encoding', '')

        if 'gzip' not in accept_encoding.lower():
            return response

        if response.mimetype not in self.app.config['GZIP_MIMETYPES']:
            return response

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
