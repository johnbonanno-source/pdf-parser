import hashlib
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import Column, DateTime, LargeBinary, MetaData, String, Table, Text, insert
from sqlalchemy.dialects.postgresql import JSONB, UUID

from db_config import get_engine

metadata = MetaData()

protocols = Table(
    "protocols",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("filename", String(255), nullable=False),
    Column("file_mime_type", String(127), nullable=False),
    Column("file_sha256", String(64), nullable=False),
    Column("source_file", LargeBinary, nullable=False),
    Column("model_name", String(128), nullable=False),
    Column("prompt_hash", String(64), nullable=False),
    Column("protocol_markdown", Text, nullable=False),
    Column("usage_metadata", JSONB, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
)


def save_protocol_parse(
    *,
    file_bytes: bytes,
    filename: str,
    file_mime_type: str,
    model_name: str,
    prompt_text: str,
    protocol_markdown: str,
    usage_metadata: dict[str, Any] | None,
) -> str:
    engine = get_engine()
    metadata.create_all(engine, tables=[protocols])

    record_id = uuid4()
    file_sha256 = hashlib.sha256(file_bytes).hexdigest()
    prompt_hash = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()

    with engine.begin() as connection:
        connection.execute(
            insert(protocols).values(
                id=record_id,
                filename=filename,
                file_mime_type=file_mime_type,
                file_sha256=file_sha256,
                source_file=file_bytes,
                model_name=model_name,
                prompt_hash=prompt_hash,
                protocol_markdown=protocol_markdown,
                usage_metadata=usage_metadata,
                created_at=datetime.now(timezone.utc),
            )
        )

    return str(record_id)
