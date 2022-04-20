import enum

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from typing import List, Dict


@dataclass
class Isolate:
    isolate_value: int


@dataclass
class WindowOrigin:
    isolate_id: int
    url: str


@dataclass
class ExecutionContext:
    isolate_id: int
    window_origin: str
    sort_index: int
    script_id: int | None
    script_url: str
    src: str


class LogType(str, enum.Enum):
    function_call = 'call'
    construction = 'new'
    getter = 'get'
    setter = 'set'


@dataclass
class LogEntry:
    context_id: int | None
    sort_index: int
    log_type: LogType
    src_offset: int
    obj: str | None
    func: str | None
    prop: str | None
    args: list[str] | None



class RelationshipType(str, enum.Enum):
    # models relationship where parent exe ctxt creates child exe ctxt
    # From Entity: Parent execution context
    # To Entity: Child exection context
    execution_hierarchy = 'exe_hierarchy'


@dataclass
class Relationship:
    relationship_type: RelationshipType
    from_entity: str | None
    to_entity: str | None


@dataclass
class ParsedLogModel:
    submission_id: int
    isolates: list[Isolate] = Field(default_factory=list)
    window_origins: list[WindowOrigin] = Field(default_factory=list)
    execution_contexts: list[ExecutionContext] = Field(default_factory=list)
    log_entries: list[LogEntry] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list, init=False)
