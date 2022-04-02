import io
import json


# Class for storing the details of a function call line in the logs
class Function:
    def __init__(self, offset, owner, name, args):
        self.offset = offset
        self.owner = owner
        self.name = name
        self.args = args

    def _to_json(self):
        return {
            'offset': self.offset,
            'owner': self.owner,
            'name': self.name,
            'args': self.args
        }

    def to_json(self):
        return json.dumps(self._to_json(), separators=(',', ':'))


# Class for storing the details of a get call line in the logs
class Get:
    def __init__(self, offset, owner, prop):
        self.offset = offset
        self.owner = owner
        self.prop = prop

    def _to_json(self):
        return {
            'offset': self.offset,
            'owner': self.owner,
            'prop': self.prop
        }

    def to_json(self):
        return json.dumps(self._to_json(), separators=(',', ':'))


# Class for storing the details of a set call line in the logs
class Set:
    def __init__(self, offset, owner, name, new_val):
        self.offset = offset
        self.owner = owner
        self.name = name
        self.new_val = new_val

    def _to_json(self):
        return {
            'offset': self.offset,
            'owner': self.owner,
            'name': self.name,
            'new_val': self.new_val
        }

    def to_json(self):
        return json.dumps(self._to_json(), separators=(',', ':'))


# Class for storing the details of a object creation line in the logs
class Object:
    def __init__(self, offset, name, args):
        self.offset = offset
        self.name = name
        self.args = args

    def _to_json(self):
        return {
            'offset': self.offset,
            'name': self.name,
            'args': self.args
        }

    def to_json(self):
        return json.dumps(self._to_json(), separators=(',', ':'))


# Class for storing a context within the tree of contexts from the logs
class Script:
    def __init__(self, num, text):
        self.num = num
        self.text = text
        self.gets = []
        self.function_calls = []
        self.objects = []
        self.sets = []
        self.children = []
        self.window_origins = []

    def _to_json(self):
        return {
            'num': self.num,
            'gets': [x._to_json() for x in self.gets],
            'function_calls': [x._to_json() for x in self.function_calls],
            'objects': [x._to_json() for x in self.objects],
            'sets': [x._to_json() for x in self.sets],
            'children': [x._to_json() for x in self.children],
            'window_origins': self.window_origins,
            'text': self.text
        }

    def to_json(self):
        return json.dumps(self._to_json(), separators=(',', ':'))


# function for finding a particular context node based on the input scriptNum target
def search_tree(root: Script, target: int):
    if root.num == target:
        return root
    elif len(root.children) == 0:
        return 0
    else:
        for child in root.children:
            result = search_tree(child, target)
            if result != 0:
                return result


# main function that takes the string contents of a log file and outputs a JSON object with all the information from the log
# Link to VV8 documentation for log entries
# https://github.com/wspr-ncsu/visiblev8/tree/master/tests
def parse_log(log_str):
    root = Script(0, "")
    current_level = root
    log_stream = io.StringIO(log_str)
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
            isolate_id = int(line, 16)
            # TODO: add an isolate object to tree
        elif tag == '@':
            # new window.origin
            # values: quoted string or "?"
            origin = line
            current_level.window_origins.append(origin)
        elif tag == '$':
            id_num, text = line.split(':', 1)
            try:
                id_num = int(id_num)
            except ValueError:
                id_num = -1
            script = Script(id_num, text)
            current_level.children.append(script)
        elif tag == 'g':
            # Property getter
            offset, owner, prop = line.split(':', 2)
            get = Get(offset, owner, name)
            current_level.gets.append(get)
        elif tag == 'n':
            offset, name, *args = line.split(':')
            obj = Object(offset, name, args)
            current_level.objects.append(obj)
        elif tag == 's':
            offset, owner, name, new_val = line.split(':', 3)
            set_obj = Set(offset, owner, name, new_val)
            current_level.sets.append(set_obj)
        elif tag == 'c':
            offset, owner, func_name, *args = line.split(':')
            func = Function(offset, owner, func_name, args)
            current_level.function_calls.append(func)
        elif tag == '!':
            try:
                id_num = int(line)
            except ValueError:
                id_num = -1
            result = search_tree(root, id_num)
            if isinstance(result, Script):
                current_level = result
        
    return root.to_json()


# function for extracting the log string from the given file for testing purposes prior to database hookup
def fileInput(filePath):
    inputFile = open(filePath, "r")
    output = logParse(inputFile.read())
    inputFile.close()
    return output


def main(filePath: str):
    outputFile = open(filePath + ".json", "w")
    outputFile.write(fileInput(filePath))
    outputFile.close()
