# Flask-Compress

[![Build](https://github.com/colour-science/flask-compress/actions/workflows/ci.yaml/badge.svg)](https://github.com/colour-science/flask-compress/actions/workflows/ci.yaml)
[![Version](https://img.shields.io/pypi/v/flask-compress.svg)](https://pypi.python.org/pypi/Flask-Compress)
[![Downloads](https://pypip.in/d/Flask-Compress/badge.png)](https://pypi.python.org/pypi/Flask-Compress)

Flask-Compress allows you to easily compress your [Flask](http://flask.pocoo.org/) application's responses with gzip, deflate or brotli. It originally started as a fork of [Flask-gzip](https://github.com/closeio/Flask-gzip).

The preferred solution is to have a server (like [Nginx](http://wiki.nginx.org/Main)) automatically compress the static files for you. If you don't have that option Flask-Compress will solve the problem for you.


## How it works

Flask-Compress both adds the various headers required for a compressed response and compresses the response data. 
This makes serving compressed static files extremely easy.

Internally, every time a request is made the extension will check if it matches one of the compressible MIME types
and whether the client and the server use some common compression algorithm, and will automatically attach the 
appropriate headers.

To determine the compression algorithm, the `Accept-Encoding` request header is inspected, respecting the
quality factor as described in [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Encoding). 
If no requested compression algorithm is supported by the server, we don't compress the response. If, on the other
hand, multiple suitable algorithms are found and are requested with the same quality factor, we choose the first one
defined in the `COMPRESS_ALGORITHM` option (see below). 


## Installation

If you use pip then installation is simply:

```shell
$ pip install --user flask-compress
```

or, if you want the latest github version:

```shell
$ pip install --user git+git://github.com/colour-science/flask-compress.git
```

You can also install Flask-Compress via Easy Install:

```shell
$ easy_install flask-compress
```


## Using Flask-Compress

### Globally

Flask-Compress is incredibly simple to use. In order to start compressing your Flask application's assets, the first thing to do is let Flask-Compress know about your [`flask.Flask`](http://flask.pocoo.org/docs/latest/api/#flask.Flask) application object.

```python
from flask import Flask
from flask_compress import Compress

app = Flask(__name__)
Compress(app)
```

In many cases, however, one cannot expect a Flask instance to be ready at import time, and a common pattern is to return a Flask instance from within a function only after other configuration details have been taken care of. In these cases, Flask-Compress provides a simple function, `flask_compress.Compress.init_app`, which takes your application as an argument.

```python
from flask import Flask
from flask_compress import Compress

compress = Compress()

def start_app():
    app = Flask(__name__)
    compress.init_app(app)
    return app
```

In terms of automatically compressing your assets, passing your [`flask.Flask`](http://flask.pocoo.org/docs/latest/api/#flask.Flask) object to the `flask_compress.Compress` object is all that needs to be done.

### Per-view compression

Compression is possible per view using the `@compress.compressed()` decorator. Make sure to disable global compression first.

```python
from flask import Flask
from flask_compress import Compress

app = Flask(__name__)
app.config["COMPRESS_REGISTER"] = False  # disable default compression of all eligible requests
compress = Compress()
compress.init_app(app)

# Compress this view specifically
@app.route("/test")
@compress.compressed()
def view():
   pass
```

## Options

Within your Flask application's settings you can provide the following settings to control the behavior of Flask-Compress. None of the settings are required.

| Option | Description | Default |
| ------ | ----------- | ------- |
| `COMPRESS_MIMETYPES` | Set the list of mimetypes to compress here. | `[`<br>`'text/html',`<br>`'text/css',`<br>`'text/xml',`<br>`'application/json',`<br>`'application/javascript'`<br>`]` |
| `COMPRESS_LEVEL` | Specifies the gzip compression level. | `6` |
| `COMPRESS_BR_LEVEL` | Specifies the Brotli compression level. Ranges from 0 to 11. | `4` |
| `COMPRESS_BR_MODE` | For Brotli, the compression mode. The options are 0, 1, or 2. These correspond to "generic", "text" (for UTF-8 input), and "font" (for WOFF 2.0). | `0` |
| `COMPRESS_BR_WINDOW` | For Brotli, this specifies the base-2 logarithm of the sliding window size. Ranges from 10 to 24. | `22` |
| `COMPRESS_BR_BLOCK` | For Brotli, this provides the base-2 logarithm of the maximum input block size. If zero is provided, value will be determined based on the quality. Ranges from 16 to 24. | `0` |
| `COMPRESS_DEFLATE_LEVEL` | Specifies the deflate compression level. | `-1` |
| `COMPRESS_MIN_SIZE` | Specifies the minimum file size threshold for compressing files. | `500` |
| `COMPRESS_CACHE_KEY` | Specifies the cache key method for lookup/storage of response data. | `None` |
| `COMPRESS_CACHE_BACKEND` | Specified the backend for storing the cached response data. | `None` |
| `COMPRESS_REGISTER` | Specifies if compression should be automatically registered. | `True` |
| `COMPRESS_ALGORITHM` | Supported compression algorithms. | `['br', 'gzip', 'deflate']` |
