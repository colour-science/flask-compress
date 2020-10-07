# Change Log for `flask-compress`
All notable changes to `flask-compress` will be documented in this file.

## [Unreleased]
### Added
- The following parameters to control Brotli compression are now available: `COMPRESSION_BR_MODE`, `COMPRESSION_BR_LEVEL`, `COMPRESS_BR_WINDOW`, `COMPRESSION_BR_BLOCK`. [#10](https://github.com/colour-science/flask-compress/pull/10)
- Add deflate support [#8](https://github.com/colour-science/flask-compress/pull/8)

### Changed
- The default quality level for Brotli is now 6, which provides compression comparable to `gzip` at the default setting, while reducing the time required versus the Brotli default of 11.

## [1.6.0] - 2020-10-05
### Added
- Support for multiple compression algorithms and quality factors [#7](https://github.com/colour-science/flask-compress/pull/7)

### Changed
- Modified default compression settings to use Brotli when available before `gzip`

## [1.5.0] - 2020-05-09
### Added
- Add Brotli support [#1](https://github.com/colour-science/flask-compress/pull/1)

## [1.4.0] - 2017-01-04

## [1.3.2] - 2016-09-28

## [1.3.1] - 2016-09-21

## [1.3.0] - 2015-10-08

## [1.2.1] - 2015-06-02

## [1.2.0] - 2015-03-27

## [1.1.1] - 2015-03-24

## [1.1.0] - 2015-02-16

## [1.0.2] - 2014-04-19

## [1.0.2] - 2014-04-19

## [1.0.1] - 2014-03-04
### Changed
- Temporarily remove test for vary header until it is fixed.

## [1.0.0] - 2013-10-28

## [0.10.0] - 2013-08-15

## [0.9.0] - 2013-08-14
### Fixed
- Fixed a runtime error when `direct_passthrough` is used.
