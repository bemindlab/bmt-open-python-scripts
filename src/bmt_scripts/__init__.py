"""
BMT Open Python Scripts
~~~~~~~~~~~~~~~~~~~~~~

Python script collection for various tasks
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("bmt-scripts")
except PackageNotFoundError:
    __version__ = "0.1.0"

__author__ = "Bemind Technology"
__email__ = "inf@bemind.tech"
