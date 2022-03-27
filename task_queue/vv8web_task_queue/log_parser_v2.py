import io
import json
import enum

from dataclasses import dataclass, field


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

    def to_json(self):
        return {
            'isolate_id': self.isolate_id,
            'window_origin': self.window_id,
            'sort_index': self.sort_index,
            'script_id': self.script_id,
            'script_url': self.script_url,
            'src': self.src
        }


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


@dataclass
class ParsedLog:
    submission_id: int
    isolates: list[Isolate] = field(default_factory=list, init=False)
    window_origins: list[WindowOrigin] = field(default_factory=list, init=False)
    execution_contexts: list[ExecutionContext] = field(default_factory=list, init=False)
    log_entries: list[LogEntry] = field(default_factory=list, init=False)

    def to_json(self):
        return {
            'submission_id': self.submission_id,
            'isolates': self.isolates,
            'window_origins': self.window_origins,
            'execution_contexts': self.execution_contexts,
            'log_entries': self.log_entries
        }


# main function that takes the string contents of a log file and outputs a JSON object with all the information from the log
# Link to VV8 documentation for log entries
# https://github.com/wspr-ncsu/visiblev8/tree/master/tests
def parse_log(log_str, submission_id):
    parsed_log = ParsedLog(submission_id)
    cur_isolate_id = None
    cur_window_origin = None
    cur_exe_context = None
    sort_index = 0
    for line_num, line in enumerate(log_stream):
        # remove new line character at the end of the line
        if line[-1] == '\n':
            line = line[:-1]
        # split tag from line
        tag = line[0]
        line = line[1:]
        if tag == '~':
            # Isolate context
            # value: hex string to uniquely identify the isolate
            cur_isolate_id = int(line, 16)
            isolate = Isolate(cur_isolate_id)
            parsed_log.isolates.append(isolate)
        elif tag == '@':
            # New window.origin
            # values: quoted string or "?"
            if line == '?':
                origin_str = None
            else:
                assert line[0] == '"'
                assert line[-1] == '"'
                origin_str = line[1:-1]
            assert cur_isolate_id is not None
            origin = WindowOrigin(cur_isolate_id, line)
            cur_window_origin = origin_str
            parsed_log.window_origins.append(origin)
        elif tag == '$':
            # Script providence
            script_id, script_url, src = line.split(':', 2)
            assert cur_isolate_id is not None
            assert cur_window_origin is not None
            exe_context = ExecutionContext(
                cur_isolate_id, cur_window_id, sort_index, script_id, script_url, src
            )
            sort_index += 1
            parsed_log.execution_contexts.append(exe_context)
        elif tag == '!':
            # Execution context
            try:
                cur_exe_context = int(line)
            except:
                # Execution context may be "?". This is usually caused by a script provance not
                # being defined before execution and/or having an unknown ("?") window origin.
                cur_exe_context = -1
        elif tag == 'c':
            # Function call
            offset, obj, func_name, *args = line.split(':')
            assert cur_exe_context is not None
            log_entry = LogEntry(
                cur_exe_context, sort_index, LogType.function_call, offset,
                obj, func_name, None, args
            )
            sort_index += 1
            parsed_log.log_entries.append(log_entry)
        elif tag == 'n':
            # Construction
            offset, con_name, *args = line.split(':')
            assert cur_exe_context is not None
            log_entry = LogEntry(
                cur_exe_context, sort_index, LogType.construction, offset,
                None, con_name, None, args
            )
            sort_index += 1
            parsed_log.log_entries.append(log_entry)
        elif tag == 'g':
            # Property getter
            offset, obj, prop = line.split(':', 2)
            assert cur_exe_context is not None
            log_entry = LogEntry(
                cur_exe_context, sort_index, LogType.getter, offset,
                obj, None, prop, None
            )
            sort_index += 1
            parsed_log.log_entries.append(log_entry)
        elif tag == 's':
            # Propery setter
            offset, obj, prop, new_val = line.split(':', 3)
            assert cur_exe_context is not None
            log_entry = LogEntry(
                cur_exe_context, sort_index, LogType.setter, offset,
                obj, None, prop, [new_val]
            )
            sort_index += 1
            parsed_log.log_entries.append(log_entry)
    return parsed_log.to_json()
