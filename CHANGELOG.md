# Changelog

All notable changes to `flask-compress` will be documented in this file.

## 1.21 (development)

- streaming is now supported:
    - the previous behavior was that is `COMPRESS_STREAMS` was `True` (the default), streaming responses were compressed in 1 sitting, meaning streaming responses were effectively not streamed, If `COMPRESS_STREAMS` was `False`, streaming responses were not compressed at all.
    - now, if `COMPRESS_STREAMS` is `True`, streaming responses are compressed on-the-fly as data is streamed, which means that streaming responses are still streamed, but compressed. If `COMPRESS_STREAMS` is `False`, streaming responses are not compressed at all, as before.
    - we have a new `COMPRESS_ALGORITHM_STREAMING` config option to specify the compression algorithm to use for streaming responses, which defaults to `["zstd", "br", "deflate"]`, as `"gzip"` is not suitable for streaming compression.

## 1.20 (2025-10-20)

- the new `COMPRESS_EVALUATE_CONDITIONAL_REQUEST` config option is now `True` by default

## 1.19 (2025-10-20)

- Use `backports.zstd` instead of `pyzstd`, [#63](https://github.com/colour-science/flask-compress/pull/63) by @alexprengere
- Add new behaviours to improve Etag compatibility,  [#67](https://github.com/colour-science/flask-compress/pull/67), by @jlopex
    - weak etags are no longer modified by flask-compress
    - add new `COMPRESS_EVALUATE_CONDITIONAL_REQUEST` config option to call `response.make_conditional(request)` after compression, this ensures that 304 Not Modified responses are correctly generated when the client sends conditional requests with `If-None-Match` (defaults to `False`)

## 1.18 (2025-07-11)

- Support, and test against, Python 3.14, see [#61](https://github.com/colour-science/flask-compress/pull/61) by @kurtmckee
- Migrate from `zstandard` to `pyzstd`, which is now included in the Python 3.14 standard library, also part of [#61](https://github.com/colour-science/flask-compress/pull/61)
- Restore `flask_compress.DictCache()` that is needed to configure Flask-Compress with caching, without relying on [Flask-Caching](https://pypi.org/project/Flask-Caching/)

## 1.17 (2024-10-14)

- Add support for Python 3.13 in tox and classifiers
- Expand mimetype defaults, see [#57](https://github.com/colour-science/flask-compress/pull/57)
- Minor performance improvements, cache the algorithm selection logic

## 1.16 (2024-10-13)

- Drop support for Python 3.8 and lower, see [#46](https://github.com/colour-science/flask-compress/pull/46)
- Fix cache pollution caused by caching compression results for different compression algorithms, see [#53](https://github.com/colour-science/flask-compress/issues/53)

## 1.15 (2024-04-24)

- Add support of Zstandard compression.

## 1.14 (2023-09-11)

- Add `text/javascript` mimetype. See [#41](https://github.com/colour-science/flask-compress/pull/41)
- Use [brotlicffi](https://github.com/python-hyper/brotlicffi) for PyPy

## 1.13 (2022-09-21)

- Re-enable compression for streaming, but hide it behind a new option `COMPRESS_STREAMS` that defaults to `True`. See [#36](https://github.com/colour-science/flask-compress/pull/36)

## 1.12 (2022-04-28)

- Disable compression when response is streamed, see [#31](https://github.com/colour-science/flask-compress/pull/31)

## 1.11 (2022-03-01)

- When compression is enabled, *accept-encoding* is always added to the `Vary` header, fixes [#28](https://github.com/colour-science/flask-compress/issues/28)

## 1.10.0 (2021-06-15)

- Automate the release process with GitHub Actions
- Use `setuptools_scm` to manage package versions
- The layout is now an actual package rather than a single module
- Clean up unused files

## 1.9.0 (2021-02-12)

- Add support for the `identity` value in *accept-encoding*, fixes [#19](https://github.com/colour-science/flask-compress/issues/19)

## 1.8.0 (2020-11-03)

- Support ETag header as defined in *RFC7232* [#17](https://github.com/colour-science/flask-compress/pull/17)
- Implement per-view compression [#14](https://github.com/colour-science/flask-compress/pull/14)

## 1.7.0 (2020-10-09)

- The following parameters to control Brotli compression are now available: [#10](https://github.com/colour-science/flask-compress/pull/10)
    - `COMPRESS_BR_MODE`
    - `COMPRESS_BR_LEVEL`
    - `COMPRESS_BR_WINDOW`
    - `COMPRESS_BR_BLOCK`
- Add deflate support, with `COMPRESS_DEFLATE_LEVEL` to control compression level (default is `-1`) [#8](https://github.com/colour-science/flask-compress/pull/8)
- The default quality level for Brotli is now `4`, which provides compression comparable to `gzip` at the default setting, while reducing the time required versus the Brotli default of `11`

## 1.6.0 (2020-10-05)

- Support for multiple compression algorithms and quality factors [#7](https://github.com/colour-science/flask-compress/pull/7)
- Modified default compression settings to use Brotli when available before `gzip`

## 1.5.0 (2020-05-09)

- Add Brotli support [#1](https://github.com/colour-science/flask-compress/pull/1)
