# compression compatibility
# -------------------------
#
# Use the Python 3.14 `compression` module if possible.
# If unavailable, mimic the module structure for backwards compatibility.
#
# When Python 3.14 is the lowest supported version,
# the `import compression.*` statements can move to `flask_compress.py`
# and this try/except block can be removed from this file.
#
# Note that some compression algorithms may not be available in all environments.
#
from __future__ import annotations
import sys
import types
import logging

logger = logging.getLogger(__name__)


def _import_optional(name: str) -> types.ModuleType | None:
    try:
        return __import__(name)
    except ImportError:
        logger.warning("Module %s is not available", name)
        return None


if sys.version_info >= (3, 14):
    import compression

    _import_optional("compression.gzip")
    _import_optional("compression.zlib")
    _import_optional("compression.zstd")
else:  # Python <= 3.13
    gzip = _import_optional("gzip")
    zlib = _import_optional("zlib")
    from backports import zstd

    compression = types.SimpleNamespace()
    compression.zstd = zstd
    if gzip is not None:
        compression.gzip = gzip
    if zlib is not None:
        compression.zlib = zlib
