"""
modules
=============

Holds basic properties used by device
"""

import os

# Pin definition by the board IO
RST_PIN = 11
DC_PIN = 22
CS_PIN = 24
BUSY_PIN = 18

__version__ = "0.000.0"

path = os.path.dirname(__file__)
"""Path to StockWatcher package directory."""

fonts_path = os.path.join(path, f"fonts{os.sep}")
"""Path to fonts directory."""
