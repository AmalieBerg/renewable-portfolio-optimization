"""
Renewable Energy Portfolio Optimization

A quantitative framework for optimizing renewable energy portfolios
in the ERCOT power market.

Author: Amalie Berg
"""

__version__ = "0.1.0"
__author__ = "Amalie Berg"

# Import main modules for easier access
from . import data_processing
from . import visualization

__all__ = [
    "data_processing",
    "visualization",
]
