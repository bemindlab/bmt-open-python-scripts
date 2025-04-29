"""
BMT Libs Package
~~~~~~~~~~~~~~~~

Reusable library modules for the project
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("bmt-scripts")
except PackageNotFoundError:
    __version__ = "0.1.0"

__author__ = "Bemind Technology"
__email__ = "inf@bemind.tech"