"""Custom exceptions for the cognee knowledge graph framework."""


class CogneeError(Exception):
    """Base exception class for all cognee errors."""

    def __init__(self, message: str = "An error occurred in cognee", *args):
        self.message = message
        super().__init__(message, *args)

    def __str__(self):
        return self.message


class ConfigurationError(CogneeError):
    """Raised when there is a configuration issue."""

    def __init__(self, message: str = "Invalid or missing configuration"):
        super().__init__(message)


class LLMError(CogneeError):
    """Raised when an LLM provider call fails."""

    def __init__(self, message: str = "LLM request failed", provider: str = None):
        self.provider = provider
        full_message = f"[{provider}] {message}" if provider else message
        super().__init__(full_message)


class VectorDBError(CogneeError):
    """Raised when a vector database operation fails."""

    def __init__(self, message: str = "Vector DB operation failed", operation: str = None):
        self.operation = operation
        full_message = f"Vector DB '{operation}' failed: {message}" if operation else message
        super().__init__(full_message)


class GraphDBError(CogneeError):
    """Raised when a graph database operation fails."""

    def __init__(self, message: str = "Graph DB operation failed", operation: str = None):
        self.operation = operation
        full_message = f"Graph DB '{operation}' failed: {message}" if operation else message
        super().__init__(full_message)


class IngestionError(CogneeError):
    """Raised when data ingestion fails."""

    def __init__(self, message: str = "Data ingestion failed", source: str = None):
        self.source = source
        full_message = f"Ingestion from '{source}' failed: {message}" if source else message
        super().__init__(full_message)


class SearchError(CogneeError):
    """Raised when a search query fails."""

    def __init__(self, message: str = "Search operation failed", query: str = None):
        self.query = query
        # Truncate long queries in the error message to keep logs readable.
        # Increased limit from 80 to 120 chars — 80 was cutting off too aggressively
        # for the longer semantic queries I tend to use.
        display_query = (query[:120] + "...") if query and len(query) > 120 else query
        full_message = f"Search failed for query '{display_query}': {message}" if display_query else message
        super().__init__(full_message)


class DatasetNotFoundError(CogneeError):
    """Raised when a requested dataset does not exist."""

    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        super().__init__(f"Dataset '{dataset_name}' not found")


class NodeNotFoundError(GraphDBError):
    """Raised when a requested graph node does not exist."""

    def __init__(self, node_id: str):
        self.node_id = node_id
        super().__init__(message=f"Node '{node_id}' not found", operation="lookup")


class AuthenticationError(CogneeError):
    """Raised when authentication with an external service fails."""

    def __init__(self, message: str = "Authentication failed", service: str = None):
        self.service = service
        full_message = f"Authentication failed for service '{service}': {message}" if service else message
        super().__init__(full_message)
