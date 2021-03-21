"""
macro-zero
================

Holds basic properties used by device

- I/O Mappings
"""

import os

__version__ = "0.000.0"

path = os.path.dirname(__file__)
"""Path to StockWatcher package directory."""

fonts_path = os.path.join(path, f"fonts{os.sep}")
"""Path to fonts directory."""
