"""Cognee - Knowledge graph and memory layer for AI applications.

This package provides tools for building, querying, and managing
knowledge graphs powered by LLMs.
"""

__version__ = "0.1.0"
__author__ = "cognee contributors"
__license__ = "Apache-2.0"

from cognee.api.v1.add import add
from cognee.api.v1.cognify import cognify
from cognee.api.v1.search import search
from cognee.api.v1.prune import prune
from cognee.config import Config

__all__ = [
    "add",
    "cognify",
    "search",
    "prune",
    "Config",
    "__version__",
]
