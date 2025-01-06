# Flask-Compress

[![Build](https://github.com/colour-science/flask-compress/actions/workflows/ci.yaml/badge.svg)](https://github.com/colour-science/flask-compress/actions/workflows/ci.yaml)
[![Version](https://img.shields.io/pypi/v/flask-compress.svg)](https://pypi.python.org/pypi/Flask-Compress)
[![Downloads](https://static.pepy.tech/badge/flask-compress)](https://pypi.python.org/pypi/Flask-Compress)

Flask-Compress allows you to easily compress your [Flask](http://flask.pocoo.org/) application's responses with gzip, deflate, brotli or zstd. It originally started as a fork of [Flask-gzip](https://github.com/closeio/Flask-gzip). Supported Python versions are 3.9 and newer.

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
$ pip install flask-compress
```

or, if you want the latest github version:

```shell
$ pip install git+git://github.com/colour-science/flask-compress.git
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

### Cache example

Flask-Compress can be integrated with caching mechanisms to serve compressed responses directly from the cache. This can significantly reduce server load and response times.
Here is an example of how to configure Flask-Compress with caching using [Flask-Caching](https://pypi.org/project/Flask-Caching/).
The example demonstrates how to create a simple cache instance with a 1-hour timeout, and use it to cache compressed responses for incoming requests.

```python
from flask import Flask
from flask_compress import Compress
from flask_cache import Cache

# Initializing flask app
app = Flask(__name__)

cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 60*60  # 1 hour cache timeout
})
cache.init_app(app)

# Define a function to return cache key for incoming requests
def get_cache_key(request):
    return request.url

# Initialize Flask-Compress
compress = Compress()
compress.init_app(app)

# Set up cache for compressed responses
compress.cache = cache
compress.cache_key = get_cache_key
```

If you do not want to pull an external dependency, you can use a simple in-memory cache using `compress.cache = flask_compress.DictCache()`.

## Options

Within your Flask application's settings you can provide the following settings to control the behavior of Flask-Compress. None of the settings are required.

| Option | Description | Default |
| ------ | ----------- | ------- |
| `COMPRESS_MIMETYPES` | Set the list of mimetypes to compress here. | `[`<br>`'text/html',`<br>`'text/css',`<br>`'text/plain',`<br>`'text/xml',`<br>`'text/x-component',`<br>`'text/javascript',`<br>`'application/x-javascript',`<br>`'application/javascript',`<br>`'application/json',`<br>`'application/manifest+json',`<br>`'application/vnd.api+json',`<br>`'application/xml',`<br>`'application/xhtml+xml',`<br>`'application/rss+xml',`<br>`'application/atom+xml',`<br>`'application/vnd.ms-fontobject',`<br>`'application/x-font-ttf',`<br>`'application/x-font-opentype',`<br>`'application/x-font-truetype',`<br>`'image/svg+xml',`<br>`'image/x-icon',`<br>`'image/vnd.microsoft.icon',`<br>`'font/ttf',`<br>`'font/eot',`<br>`'font/otf',`<br>`'font/opentype',`<br>`]` |
| `COMPRESS_LEVEL` | Specifies the gzip compression level. | `6` |
| `COMPRESS_BR_LEVEL` | Specifies the Brotli compression level. Ranges from 0 to 11. | `4` |
| `COMPRESS_BR_MODE` | For Brotli, the compression mode. The options are 0, 1, or 2. These correspond to "generic", "text" (for UTF-8 input), and "font" (for WOFF 2.0). | `0` |
| `COMPRESS_BR_WINDOW` | For Brotli, this specifies the base-2 logarithm of the sliding window size. Ranges from 10 to 24. | `22` |
| `COMPRESS_BR_BLOCK` | For Brotli, this provides the base-2 logarithm of the maximum input block size. If zero is provided, value will be determined based on the quality. Ranges from 16 to 24. | `0` |
| `COMPRESS_ZSTD_LEVEL` | Specifies the ZStandard compression level. Ranges from 1 to 22. Levels >= 20, labeled ultra, should be used with caution, as they require more memory. 0 means use the default level. -131072 to -1, negative levels extend the range of speed vs ratio preferences. The lower the level, the faster the speed, but at the cost of compression ratio. | `3` |
| `COMPRESS_DEFLATE_LEVEL` | Specifies the deflate compression level. | `-1` |
| `COMPRESS_MIN_SIZE` | Specifies the minimum file size threshold for compressing files. | `500` |
| `COMPRESS_CACHE_KEY` | Specifies the cache key method for lookup/storage of response data. | `None` |
| `COMPRESS_CACHE_BACKEND` | Specified the backend for storing the cached response data. | `None` |
| `COMPRESS_REGISTER` | Specifies if compression should be automatically registered. | `True` |
| `COMPRESS_ALGORITHM` | Supported compression algorithms. | `['zstd', 'br', 'gzip', 'deflate']` |
| `COMPRESS_STREAMS` | Compress content streams. | `True` |
