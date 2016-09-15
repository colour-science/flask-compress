Flask-Compress
**************
.. module:: flask_compress

Flask-Compress allows you to easily compress your `Flask`_ application's
responses with gzip.

The preferred solution is to have a server (like `Nginx`_) automatically
compress the static files for you. If you don't have that option Flask-Compress
will solve the problem for you.

.. _Flask: http://flask.pocoo.org/
.. _Nginx: http://wiki.nginx.org/Main


How it works
============

Flask-Compress both adds the various headers required for a compressed response
and gzips the response data. This makes serving gzip compressed static files
extremely easy.

Internally, every time a request is made the extension will check if it matches
one of the compressible MIME types and automatically attach the appropriate
headers.


Installation
============

If you use pip then installation is simply:

.. code-block:: bash

    > pip install flask-compress

or, if you want the latest github version:

.. code-block:: bash

    > pip install git+git://github.com/wichitacode/flask-compress.git

You can also install Flask-Compress via Easy Install:

.. code-block:: bash

    > easy_install flask-compress


Using Flask-Compress
====================

Flask-Compress is incredibly simple to use. In order to start gzip'ing your
Flask application's assets, the first thing to do is let Flask-Compress know
about your :class:`flask.Flask` application object.

.. code-block:: python

    from flask import Flask
    from flask_compress import Compress

    app = Flask(__name__)
    Compress(app)

In many cases, however, one cannot expect a Flask instance to be ready
at import time, and a common pattern is to return a Flask instance from
within a function only after other configuration details have been taken
care of. In these cases, Flask-Compress provides a simple function,
``init_app``, which takes your application as an argument.

.. code-block:: python

    from flask import Flask
    from flask_compress import Compress

    compress = Compress()

    def start_app():
        app = Flask(__name__)
        compress.init_app(app)
        return app

In terms of automatically compressing your assets using gzip, passing your
``Flask`` object to the ``Compress`` object is all that needs to be done.


Flask-Compress Options
----------------------

Within your Flask application's settings you can provide the following
settings to control the behaviour of Flask-Compress. None of the settings are
required.

=========================== ===================================================
`COMPRESS_MIMETYPES`        Set the list of mimetypes to compress here.
                            **Default:** `['text/html', 'text/css', 'text/xml',
                            'application/json', 'application/javascript']`
`COMPRESS_LEVEL`            Specifies the gzip compression level.
                            **Default:** `6`
`COMPRESS_MIN_SIZE`         Specifies the minimum file size threshold for
                            compressing files.
                            **Default:** `500`
=========================== ===================================================


API Documentation
=================

Flask-Compress is a very simple extension. The few exposed objects, methods
and functions are as follows.

The Compress Object
-------------------
.. autoclass:: Compress

    .. automethod:: init_app
    .. automethod:: after_request
