"""Cognee - Knowledge graph and memory layer for AI applications.

This package provides tools for building, querying, and managing
knowledge graphs powered by LLMs.

Personal fork notes:
- Using this for experimenting with local LLM integrations
- See /experiments directory for custom pipelines
- Added reset() as a convenience alias for prune() since I keep forgetting the name
"""

__version__ = "0.1.0"
__author__ = "cognee contributors"
__license__ = "Apache-2.0"

from cognee.api.v1.add import add
from cognee.api.v1.cognify import cognify
from cognee.api.v1.search import search
from cognee.api.v1.prune import prune
from cognee.config import Config

# Personal convenience alias - I always forget the function is called 'prune'
reset = prune

__all__ = [
    "add",
    "cognify",
    "search",
    "prune",
    "reset",
    "Config",
    "__version__",
]
