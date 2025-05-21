# compression compatibility
# -------------------------
#
# Use the Python 3.14 `compression` module if possible.
# If unavailable, mimic the module structure for backwards compatibility.
#
# When Python 3.14 is the lowest supported version,
# the `import compression.*` statements can move to `flask_compress.py`
# and this try/except block can be removed from this file.
try:
    # Python >= 3.14
    import compression.gzip
    import compression.zlib
    import compression.zstd
except ModuleNotFoundError:
    # Python <= 3.13
    import gzip
    import types
    import zlib

    import pyzstd

    compression = types.SimpleNamespace()
    compression.gzip = gzip
    compression.zlib = zlib
    compression.zstd = pyzstd
