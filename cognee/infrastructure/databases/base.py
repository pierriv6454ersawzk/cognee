"""Base database interface definitions for cognee.

This module provides abstract base classes that all database adapters
(vector, graph, relational) must implement, ensuring a consistent API
across different storage backends.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


class BaseDatabase(ABC):
    """Abstract base class for all database adapters."""

    @abstractmethod
    async def connect(self) -> None:
        """Establish a connection to the database."""
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self) -> None:
        """Close the database connection gracefully."""
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """Return True if the database is reachable and healthy."""
        raise NotImplementedError


class BaseVectorDatabase(BaseDatabase):
    """Abstract base class for vector/embedding store adapters."""

    @abstractmethod
    async def create_collection(
        self,
        collection_name: str,
        dimension: int,
        distance_metric: str = "cosine",
    ) -> None:
        """Create a new vector collection (index)."""
        raise NotImplementedError

    @abstractmethod
    async def delete_collection(self, collection_name: str) -> None:
        """Delete an existing vector collection."""
        raise NotImplementedError

    @abstractmethod
    async def upsert(
        self,
        collection_name: str,
        vectors: List[Dict[str, Any]],
    ) -> None:
        """Insert or update vectors in a collection.

        Each item in *vectors* should have at least:
            - ``id``: unique identifier (str or int)
            - ``vector``: list of floats
            - ``payload``: optional dict of metadata
        """
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        collection_name: str,
        query_vector: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Return the *top_k* nearest neighbours to *query_vector*."""
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        collection_name: str,
        ids: List[str],
    ) -> None:
        """Remove vectors by their IDs from a collection."""
        raise NotImplementedError


class BaseGraphDatabase(BaseDatabase):
    """Abstract base class for graph database adapters."""

    @abstractmethod
    async def add_node(
        self,
        node_id: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add or update a node with the given properties."""
        raise NotImplementedError

    @abstractmethod
    async def add_edge(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add or update a directed edge between two nodes."""
        raise NotImplementedError

    @abstractmethod
    async def get_neighbours(
        self,
        node_id: str,
        relationship_type: Optional[str] = None,
        depth: int = 1,
    ) -> List[Dict[str, Any]]:
        """Return neighbouring nodes, optionally filtered by relationship type."""
        raise NotImplementedError

    @abstractmethod
    async def delete_node(self, node_id: str) -> None:
        """Remove a node and all its edges from the graph."""
        raise NotImplementedError

    @abstractmethod
    async def query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Execute a raw graph query (e.g. Cypher, Gremlin) and return results."""
        raise NotImplementedError
