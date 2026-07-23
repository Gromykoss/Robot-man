"""Pydantic schema for Knowledge Graph — Anthropic Graph Engineering Playbook, Steps 1-3.
Strict models ensure Claude/DeepSeek outputs valid structured data.
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional
import uuid


class Entity(BaseModel):
    """A node in the knowledge graph — person, project, event, task, etc."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str
    type: str  # person, project, event, task, decision, file
    description: Optional[str] = None
    source_file: str  # where it was extracted from
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Triple(BaseModel):
    """Subject-Predicate-Object triple with provenance — Step 2: strict schema."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    subject: str
    predicate: str  # occurred_on, described_as, mentioned_in, referenced_in, decided, depends_on
    object: str
    provenance: str  # source file path
    line_hint: Optional[int] = None
    confidence: float = Field(ge=0.0, le=1.0, default=0.85)
    extracted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @field_validator("confidence")
    @classmethod
    def clamp_confidence(cls, v: float) -> float:
        return max(0.0, min(1.0, v))


class Edge(BaseModel):
    """Graph edge — the assembled version of a Triple after resolution."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    source_node: str
    target_node: str
    predicate: str
    triples: list[str] = Field(default_factory=list)  # triple IDs that support this edge
    source_files: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.85)
    assembled_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class GraphQuery(BaseModel):
    """A query against the knowledge graph — Step 10."""
    question: str
    center_entity: Optional[str] = None
    max_hops: int = Field(default=2, ge=1, le=5)
    max_triples: int = Field(default=20, ge=1, le=100)


class GraphAnswer(BaseModel):
    """The answer from querying the graph — Step 11: every answer cites edges."""
    question: str
    answer: str
    cited_edges: list[str] = Field(default_factory=list)  # edge IDs
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    graph_snapshot_built: Optional[str] = None
