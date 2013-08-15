Flask-Gzip
**********
.. module:: flask_gzip

Flask-Gzip allows you to easily compress your `Flask`_ application's
responses with gzip.

The preferred solution is to have a server (like `Nginx`_) automatically
compress the static files for you. If you don't have that option Flask-Gzip
will solve the problem for you.

.. _Flask: http://flask.pocoo.org/
.. _Nginx: http://wiki.nginx.org/Main


How it works
============

Flask-Gzip both adds the various headers required for a compressed response and
gzips the response data. This makes serving gzip compressed static files
extremely easy.

Internally, every time a request is made the extension will check if it matches
one of the compressable mimetypes and automatically attach the appropriate
headers.


Installation
============

If you use pip then installation is simply::

    $ pip install flask-gzip

or, if you want the latest github version::

    $ pip install git+git://github.com/wichitacode/flask-gzip.git

You can also install Flask-Gzip via Easy Install::

    $ easy_install flask-gzip

Dependencies
------------

There are no additional dependencies besides Flask itself.


Using Flask-Gzip
================

Flask-Gzip is incredibly simple to use. In order to start gzip'ing your
Flask application's assets, the first thing to do is let Flask-Gzip know about
your :class:`flask.Flask` application object.

.. code-block:: python

    from flask import Flask
    from flask.ext.gzip import Gzip

    app = Flask(__name__)
    Gzip(app)

In many cases, however, one cannot expect a Flask instance to be ready
at import time, and a common pattern is to return a Flask instance from
within a function only after other configuration details have been taken
care of. In these cases, Flask-Gzip provides a simple function,
``init_app``, which takes your application as an argument.

.. code-block:: python

    from flask import Flask
    from flask.ext.gzip import Gzip

    gzip = Gzip()

    def start_app():
        app = Flask(__name__)
        gzip.init_app(app)
        return app

In terms of automatically compressing your assets using gzip, passing your
``Flask`` object to the ``Gzip`` object is all that needs to be done.


Flask-Gzip Options
------------------

Within your Flask application's settings you can provide the following
settings to control the behaviour of Flask-Gzip. None of the settings are
required.

=========================== ===================================================
`GZIP_MIMETYPES`            Set the list of mimetypes to compress here.
                            **Default:** `['text/html', 'text/css', 'text/xml',
                            'application/json', 'application/javascript']`
`GZIP_LEVEL`                Specifies the gzip compression level.
                            **Default:** `6`
`GZIP_MIN_SIZE`             Specifies the minimum file size threshold for
                            compressing files.
                            **Default:** `500`
`GZIP_DEBUG`                By default, Flask-Gzip will be switched off when
                            running your application in `debug`_ mode, so that
                            your responses are not compressed. If you wish to
                            enable Flask-Gzip in debug mode, set this value to
                            `True`.
                            **Default:** `False`
=========================== ===================================================

.. _debug: http://flask.pocoo.org/docs/config/#configuration-basics


API Documentation
=================

Flask-Gzip is a very simple extension. The few exposed objects, methods
and functions are as follows.

The Gzip Object
------------------
.. autoclass:: Gzip

    .. automethod:: init_app
    .. automethod:: after_request
