# Authors: William Fagan
# Copyright (c) 2013-2017 William Fagan
# License: The MIT License (MIT)

import functools
from collections import defaultdict
from functools import lru_cache

try:
    import brotlicffi as brotli
except ImportError:
    import brotli

from flask import after_this_request, current_app, request, stream_with_context

from .compat import compression


class DictCache:

    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value


@lru_cache(maxsize=128)
def _choose_algorithm(algorithms, accept_encoding):
    """
    Determine which compression algorithm we're going to use based on the
    client request. The `Accept-Encoding` header may list one or more desired
    algorithms, together with a "quality factor" for each one (higher quality
    means the client prefers that algorithm more).

    :param algorithms: Tuple of supported compression algorithms
    :param accept_encoding: Content of the `Accept-Encoding` header
    :return: name of a compression algorithm (`gzip`, `deflate`, `br`, 'zstd')
        or `None` if the client and server don't agree on any.
    """
    # A flag denoting that client requested using any (`*`) algorithm,
    # in case a specific one is not supported by the server
    fallback_to_any = False

    # Map quality factors to requested algorithm names.
    algos_by_quality = defaultdict(set)

    # Set of supported algorithms
    server_algos_set = set(algorithms)

    for part in accept_encoding.lower().split(","):
        part = part.strip()
        if ";q=" in part:
            # If the client associated a quality factor with an algorithm,
            # try to parse it. We could do the matching using a regex, but
            # the format is so simple that it would be overkill.
            algo = part.split(";")[0].strip()
            try:
                quality = float(part.split("=")[1].strip())
            except ValueError:
                quality = 1.0
        else:
            # Otherwise, use the default quality
            algo = part
            quality = 1.0

        if algo == "*":
            if quality > 0:
                fallback_to_any = True
        elif algo == "identity":  # identity means 'no compression asked'
            algos_by_quality[quality].add(None)
        elif algo in server_algos_set:
            algos_by_quality[quality].add(algo)

    # Choose the algorithm with the highest quality factor that the server supports.
    #
    # If there are multiple equally good options,
    # choose the first supported algorithm from server configuration.
    #
    # If the server doesn't support any algorithm that the client requested but
    # there's a special wildcard algorithm request (`*`), choose the first supported
    # algorithm.
    for _, viable_algos in sorted(algos_by_quality.items(), reverse=True):
        if len(viable_algos) == 1:
            return viable_algos.pop()
        elif len(viable_algos) > 1:
            for server_algo in algorithms:
                if server_algo in viable_algos:
                    return server_algo

    if fallback_to_any:
        return algorithms[0]
    return None


def _format(algo):
    """Format the algorithm configuration into a tuple of strings.

    >>> _format("gzip, deflate, br")
    ('gzip', 'deflate', 'br')
    >>> _format(["gzip", "deflate", "br"])
    ('gzip', 'deflate', 'br')
    """
    if isinstance(algo, str):
        return tuple(i.strip() for i in algo.split(","))
    else:
        return tuple(algo)


class Compress:
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
            (
                "COMPRESS_MIMETYPES",
                [
                    "text/html",
                    "text/css",
                    "text/plain",
                    "text/xml",
                    "text/x-component",
                    "text/javascript",  # Obsolete (RFC 9239)
                    "application/x-javascript",
                    "application/javascript",
                    "application/json",
                    "application/manifest+json",
                    "application/vnd.api+json",
                    "application/xml",
                    "application/xhtml+xml",
                    "application/rss+xml",
                    "application/atom+xml",
                    "application/vnd.ms-fontobject",
                    "application/x-font-ttf",
                    "application/x-font-opentype",
                    "application/x-font-truetype",
                    "image/svg+xml",
                    "image/x-icon",
                    "image/vnd.microsoft.icon",
                    "font/ttf",
                    "font/eot",
                    "font/otf",
                    "font/opentype",
                ],
            ),
            ("COMPRESS_LEVEL", 6),
            ("COMPRESS_BR_LEVEL", 4),
            ("COMPRESS_BR_MODE", 0),
            ("COMPRESS_BR_WINDOW", 22),
            ("COMPRESS_BR_BLOCK", 0),
            ("COMPRESS_ZSTD_LEVEL", 3),
            ("COMPRESS_DEFLATE_LEVEL", -1),
            ("COMPRESS_MIN_SIZE", 500),
            ("COMPRESS_CACHE_KEY", None),
            ("COMPRESS_CACHE_BACKEND", None),
            ("COMPRESS_REGISTER", True),
            ("COMPRESS_STREAMS", True),
            ("COMPRESS_EVALUATE_CONDITIONAL_REQUEST", True),
            ("COMPRESS_STREAMING_ENDPOINT_CONDITIONAL", ["static"]),
            ("COMPRESS_ALGORITHM", ["zstd", "br", "gzip", "deflate"]),
            ("COMPRESS_ALGORITHM_STREAMING", ["zstd", "br", "deflate"]),  # no gzip
        ]

        for k, v in defaults:
            app.config.setdefault(k, v)

        backend = app.config["COMPRESS_CACHE_BACKEND"]
        self.cache = backend() if backend else None
        self.cache_key = app.config["COMPRESS_CACHE_KEY"]

        self.compress_mimetypes_set = set(app.config["COMPRESS_MIMETYPES"])
        self.enabled_algorithms = _format(app.config["COMPRESS_ALGORITHM"])
        self.streaming_algorithms = _format(app.config["COMPRESS_ALGORITHM_STREAMING"])
        self.streaming_endpoint_with_conditional = set(
            app.config["COMPRESS_STREAMING_ENDPOINT_CONDITIONAL"]
        )

        if app.config["COMPRESS_REGISTER"] and app.config["COMPRESS_MIMETYPES"]:
            app.after_request(self.after_request)

    def after_request(self, response):
        app = self.app or current_app

        vary = response.headers.get("Vary")
        if not vary:
            response.headers["Vary"] = "Accept-Encoding"
        elif "accept-encoding" not in vary.lower():
            response.headers["Vary"] = f"{vary}, Accept-Encoding"

        accept_encoding = request.headers.get("Accept-Encoding", "")
        streaming_compressed = response.is_streamed and app.config["COMPRESS_STREAMS"]
        streaming_conditional = response.is_streamed and (
            request.endpoint in self.streaming_endpoint_with_conditional
        )
        algorithms = (
            self.streaming_algorithms
            if streaming_compressed
            else self.enabled_algorithms
        )
        chosen_algorithm = _choose_algorithm(algorithms, accept_encoding)

        if (
            chosen_algorithm is None
            or response.mimetype not in self.compress_mimetypes_set
            or response.status_code < 200
            or response.status_code >= 300
            or (response.is_streamed and not app.config["COMPRESS_STREAMS"])
            or "Content-Encoding" in response.headers
            or (
                response.content_length is not None
                and response.content_length < app.config["COMPRESS_MIN_SIZE"]
            )
        ):
            return response

        response.direct_passthrough = False
        response.headers["Content-Encoding"] = chosen_algorithm

        if streaming_compressed:
            chunks = response.iter_encoded()
            _gen_compressed_content = _compress_chunks(app, chunks, chosen_algorithm)
            response.response = stream_with_context(_gen_compressed_content)
            response.headers.pop("Content-Length", None)
        else:
            if self.cache is not None:
                key = f"{chosen_algorithm};{self.cache_key(request)}"
                compressed_content = self.cache.get(key)
                if compressed_content is None:
                    data = response.get_data()
                    compressed_content = _compress_data(app, data, chosen_algorithm)
                self.cache.set(key, compressed_content)
            else:
                data = response.get_data()
                compressed_content = _compress_data(app, data, chosen_algorithm)

            response.set_data(compressed_content)
            response.headers["Content-Length"] = response.content_length

        # "123456789"   => "123456789:gzip"   - A strong ETag validator
        # W/"123456789" => W/"123456789:gzip" - A weak ETag validator
        etag, is_weak = response.get_etag()

        if etag and not is_weak:
            response.set_etag(f"{etag}:{chosen_algorithm}", weak=is_weak)

        if (
            app.config["COMPRESS_EVALUATE_CONDITIONAL_REQUEST"]
            and request.method in ("GET", "HEAD")
            and (not response.is_streamed or streaming_conditional)
        ):
            response.make_conditional(request)

        return response

    def compressed(self):
        def decorator(f):
            @functools.wraps(f)
            def decorated_function(*args, **kwargs):
                @after_this_request
                def compressor(response):
                    return self.after_request(response)

                return f(*args, **kwargs)

            return decorated_function

        return decorator


def _compress_data(app, data, algorithm):
    if algorithm == "zstd":
        return compression.zstd.compress(data, app.config["COMPRESS_ZSTD_LEVEL"])

    if algorithm == "gzip":
        return compression.gzip.compress(data, app.config["COMPRESS_LEVEL"])

    if algorithm == "deflate":
        return compression.zlib.compress(data, app.config["COMPRESS_DEFLATE_LEVEL"])

    if algorithm == "br":
        return brotli.compress(
            data,
            mode=app.config["COMPRESS_BR_MODE"],
            quality=app.config["COMPRESS_BR_LEVEL"],
            lgwin=app.config["COMPRESS_BR_WINDOW"],
            lgblock=app.config["COMPRESS_BR_BLOCK"],
        )

    raise ValueError(f"Unknown compression algorithm: {algorithm}")


def _uncompress_data(data, algorithm):
    # This is used for tests purposes only.
    if algorithm == "zstd":
        return compression.zstd.decompress(data)
    if algorithm == "gzip":
        return compression.gzip.decompress(data)
    if algorithm == "deflate":
        return compression.zlib.decompress(data)
    if algorithm == "br":
        return brotli.decompress(data)

    raise ValueError(f"Unknown compression algorithm: {algorithm}")


def _compress_chunks(app, chunks, algorithm):
    if algorithm == "zstd":
        level = app.config["COMPRESS_ZSTD_LEVEL"]
        compressor = compression.zstd.ZstdCompressor(level=level)
        for data in chunks:
            out = compressor.compress(data)
            if out:
                yield out
        out = compressor.flush()
        if out:
            yield out

    elif algorithm == "gzip":
        level = app.config["COMPRESS_LEVEL"]
        compressor = compression.zlib.compressobj(
            level,
            compression.zlib.DEFLATED,
            compression.zlib.MAX_WBITS + 16,
        )
        for data in chunks:
            out = compressor.compress(data)
            if out:
                yield out
        out = compressor.flush()
        if out:
            yield out

    elif algorithm == "deflate":
        level = app.config["COMPRESS_DEFLATE_LEVEL"]
        compressor = compression.zlib.compressobj(level=level)
        for data in chunks:
            out = compressor.compress(data)
            if out:
                yield out
        out = compressor.flush()
        if out:
            yield out

    elif algorithm == "br":
        compressor = brotli.Compressor(
            mode=app.config["COMPRESS_BR_MODE"],
            quality=app.config["COMPRESS_BR_LEVEL"],
            lgwin=app.config["COMPRESS_BR_WINDOW"],
            lgblock=app.config["COMPRESS_BR_BLOCK"],
        )
        for data in chunks:
            out = compressor.process(data)
            if out:
                yield out
        out = compressor.finish()
        if out:
            yield out
    else:
        raise ValueError(f"Unsupported streaming algorithm: {algorithm}")
