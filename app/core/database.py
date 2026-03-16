from __future__ import annotations

import logging

from .config import settings
from .types import IOClient, IODatabase

logger = logging.getLogger(__name__)

_client: IOClient | None = None
_db: IODatabase | None = None

def connect_to_mongo() -> None:
    global _client, _db

    _client = IOClient(settings.mongodb_url)
    _db = _client[settings.mongodb_db]

    logger.info("MongoDB connected")

def close_mongo_connection() -> None:
    global _client

    if _client:
        _client.close()
        logger.info("MongoDB disconnected")

def get_database() -> IODatabase:
    if _db is None:
        raise RuntimeError("Database not initialized")

    return _db