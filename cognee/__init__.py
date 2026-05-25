"""Cognee - Knowledge graph and memory layer for AI applications.

This package provides tools for building, querying, and managing
knowledge graphs powered by LLMs.

Personal fork notes:
- Using this for experimenting with local LLM integrations
- See /experiments directory for custom pipelines
- Added reset() as a convenience alias for prune() since I keep forgetting the name
- Added get_version() helper for quick version checks in notebooks
- Added search_and_print() helper for quick interactive exploration
- search_and_print() now defaults to GRAPH_COMPLETION for richer answers
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


def get_version() -> str:
    """Return the current version string. Handy for quick checks in notebooks."""
    return __version__


async def search_and_print(query: str, query_type: str = "GRAPH_COMPLETION") -> None:
    """Run a search and pretty-print results. Useful for quick exploration in notebooks.

    Changed default query_type from INSIGHTS to GRAPH_COMPLETION because it tends
    to give more complete, readable answers when exploring a knowledge graph interactively.
    """
    results = await search(query_type=query_type, query_text=query)
    for i, result in enumerate(results, 1):
        print(f"[{i}] {result}")


__all__ = [
    "add",
    "cognify",
    "search",
    "search_and_print",
    "prune",
    "reset",
    "get_version",
    "Config",
    "__version__",
]
