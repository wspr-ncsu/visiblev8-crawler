import enum

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from typing import List, Dict


@dataclass
class Isolate:
    isolate_id_value: int

    def to_json(self):
        return {'isolate_id_value': self.isolate_id_value}


@dataclass
class WindowOrigin:
    isolate_id: int
    url: str

    def to_json(self):
        return {
            'isolate_id': self.isolate_id,
            'url': self.url
        }


@dataclass
class ExecutionContext:
    isolate_id: int
    window_origin: str
    sort_index: int
    script_id: str
    script_url: str
    src: str


class LogType(str, enum.Enum):
    function_call = 'call'
    construction = 'new'
    getter = 'get'
    setter = 'set'


@dataclass
class LogEntry:
    context_id: int
    sort_index: int
    log_type: LogType
    src_offset: int
    obj: str
    func: str
    prop: str
    args: list[str]

    def to_json(self):
        return {
            'context_id': self.context_id,
            'sort_index': self.sort_index,
            'log_type': str(self.log_type),
            'src_offset': self.src_offset,
            'object': self.obj,
            'function': self.func,
            'property': self.prop,
            'arguments': self.args
        }

class ParsedLogModel(BaseModel):
    submission_id: int
    isolates: list[dict] = Field(default_factory=list)
    window_origins: list[dict] = Field(default_factory=list)
    execution_contexts: list[dict] = Field(default_factory=list)
    log_entries: list[LogEntry] = Field(default_factory=list)
