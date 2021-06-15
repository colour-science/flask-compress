# Changelog

All notable changes to `flask-compress` will be documented in this file.

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
