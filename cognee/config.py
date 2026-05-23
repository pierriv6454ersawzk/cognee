"""Configuration management for cognee.

This module handles loading and validation of configuration settings
from environment variables and .env files.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).parent.parent / ".env"
    if _env_path.exists():
        load_dotenv(dotenv_path=_env_path)
    else:
        load_dotenv()  # Fall back to searching default locations
except ImportError:
    pass  # dotenv not installed, rely on system environment variables


@dataclass
class LLMConfig:
    """Configuration for the language model provider."""
    provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "openai"))
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o-mini"))
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY"))
    api_base: Optional[str] = field(default_factory=lambda: os.getenv("LLM_API_BASE"))
    temperature: float = field(default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0.0")))
    max_tokens: int = field(default_factory=lambda: int(os.getenv("LLM_MAX_TOKENS", "4096")))


@dataclass
class VectorDBConfig:
    """Configuration for the vector database backend."""
    provider: str = field(default_factory=lambda: os.getenv("VECTOR_DB_PROVIDER", "qdrant"))
    url: Optional[str] = field(default_factory=lambda: os.getenv("VECTOR_DB_URL", "http://localhost:6333"))
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("VECTOR_DB_API_KEY"))
    collection_name: str = field(default_factory=lambda: os.getenv("VECTOR_DB_COLLECTION", "cognee"))
    embedding_dimensions: int = field(default_factory=lambda: int(os.getenv("EMBEDDING_DIMENSIONS", "1536")))


@dataclass
class GraphDBConfig:
    """Configuration for the graph database backend."""
    provider: str = field(default_factory=lambda: os.getenv("GRAPH_DB_PROVIDER", "networkx"))
    url: Optional[str] = field(default_factory=lambda: os.getenv("GRAPH_DB_URL"))
    username: Optional[str] = field(default_factory=lambda: os.getenv("GRAPH_DB_USERNAME"))
    password: Optional[str] = field(default_factory=lambda: os.getenv("GRAPH_DB_PASSWORD"))
    database: str = field(default_factory=lambda: os.getenv("GRAPH_DB_NAME", "cognee"))


@dataclass
class StorageConfig:
    """Configuration for local data storage."""
    data_root_dir: str = field(
        default_factory=lambda: os.getenv(
            "DATA_ROOT_DIR",
            str(Path.home() / ".cognee" / "data")
        )
    )
    db_path: str = field(
        default_factory=lambda: os.getenv(
            "DB_PATH",
            str(Path.home() / ".cognee" / "cognee.db")
        )
    )

    def ensure_dirs(self) -> None:
        """Create storage directories if they do not exist."""
        Path(self.data_root_dir).mkdir(parents=True, exist_ok=True)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)


@dataclass
class Config:
    """Top-level cognee configuration aggregating all sub-configs."""
    llm: LLMConfig = field(default_factory=LLMConfig)
    vector_db: VectorDBConfig = field(default_factory=VectorDBConfig)
    graph_db: GraphDBConfig = field(default_factory=GraphDBConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)

    # General settings
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    environment: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))

    def validate(self) -> None:
        """Validate critical configuration values and raise errors for missing required fields."""
        if not self.llm.api_key:
            raise ValueError(
                "LLM API key is not set. "
                "Please set LLM_API_KEY or OPENAI_API_KEY in your environment or .env file."
            )


# Module-level singleton instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Return the global Config singleton, creating it on first call."""
    global _config
    if _config is None:
        _config = Config()
        _config.storage.ensure_dirs()
    return _config


def reset_config() -> None:
    """Reset the global Config singleton (useful for testing)."""
    global _config
    _config = None
