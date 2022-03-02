import io
import json


class Function:
    def __init__(self, offset, name, receiver, other):
        self.offset = offset
        self.name = name
        self.receiver = receiver
        self.other = other

    def _toJSON(self):
        return {
            'offset': self.offset,
            'name': self.name,
            'receiver': self.receiver,
            'other': self.other
        }

    def toJSON(self):
        return json.dumps(self._toJSON())


class Get:
    def __init__(self, offset, owner, name):
        self.offset = offset
        self.name = name
        self.owner = owner

    def _toJSON(self):
        return {
            'offset': self.offset,
            'name': self.name,
            'owner': self.owner
        }

    def toJSON(self):
        return json.dumps(self._toJSON())


class Set:
    def __init__(self, offset, owner, name, newVal):
        self.offset = offset
        self.name = name
        self.owner = owner
        self.newVal = newVal

    def _toJSON(self):
        return {
            'offset': self.offset,
            'name': self.name,
            'owner': self.owner,
            'newVal': self.newVal
        }

    def toJSON(self):
        return json.dumps(self._toJSON())


class Object:
    def __init__(self, offset, name, other):
        self.offset = offset
        self.name = name
        self.other = other

    def _toJSON(self):
        return {
            'offset': self.offset,
            'name': self.name,
            'other': self.other
        }

    def toJSON(self):
        return json.dumps(self._toJSON())


class Script:
    def __init__(self, i, text):
        self.scriptNum = i
        self.scriptText = text
        self.gets = []
        self.functionCalls = []
        self.objects = []
        self.sets = []
        self.children = []
        self.windowOrigins = []

    def _toJSON(self):
        return {
            'scriptNum': self.scriptNum,
            'gets': [x._toJSON() for x in self.gets],
            'functionCalls': [x._toJSON() for x in self.functionCalls],
            'objects': [x._toJSON() for x in self.objects],
            'sets': [x._toJSON() for x in self.sets],
            'children': [x._toJSON() for x in self.children],
            'windowOrigins': self.windowOrigins,
            'scriptText': self.scriptText
        }

    def toJSON(self):
        return json.dumps(self._toJSON())


def searchTree(root: Script, target: int):
    if root.scriptNum == target:
        return root
    elif root.children.__len__() == 0:
        return 0
    else:
        for child in root.children:
            result = searchTree(child, target)
            if result != 0:
                return result


def logParse(logString):
    root: Script = Script(0, "")
    currentLevel: Script = root
    logIterator = io.StringIO(logString)
    for line in logIterator:
        if line[0] == 'g':
            part = line[1:line.__len__()].partition(":")
            part2 = part[2].partition(":")
            offset = part[0]
            name = part2[0]
            other = part2[2]
            currentLevel.gets.append(Get(offset, name, other[:other.__len__() - 1]))

        elif line[0] == 'n':
            part = line[1:line.__len__()].partition(":")
            part2 = part[2].partition(":")
            offset = part[0]
            name = part2[0]
            other = part2[2]
            currentLevel.objects.append(Object(offset, name, other[:other.__len__() - 1]))

        elif line[0] == 's':
            part = line[1:line.__len__()].partition(":")
            part2 = part[2].partition(":")
            part3 = part2[2].partition(":")
            offset = part[0]
            owner = part2[0]
            name = part3[0]
            newVal = part3[2]
            currentLevel.sets.append(Set(offset, owner, name, newVal[:newVal.__len__() - 1]))

        elif line[0] == 'c':

            part = line[1:line.__len__()].partition(":")
            part2 = part[2].partition(":")
            part3 = part2[2].partition(":")
            offset = part[0]
            name = part2[0]
            receiver = part3[0]
            other = part3[2]
            currentLevel.functionCalls.append(Function(offset, name, receiver, other[:other.__len__() - 1]))

        elif line[0] == '$':
            i = 1
            while line[i] != ':':
                i += 1
            try:
                idNumber = int(line[1:i])
            except ValueError:
                idNumber = -1
            newScript = Script(idNumber, line[i+1:line.__len__() - 1])
            currentLevel.children.append(newScript)

        elif line[0] == '!':
            try:
                idNumber = int(line[1:])
            except ValueError:
                idNumber = -1
            result = searchTree(root, idNumber)
            if isinstance(result, Script):
                currentLevel = result

        elif line[0] == '@':
            currentLevel.windowOrigins.append(line[2:line.__len__() - 2])

    return root.toJSON()


def fileInput(filePath):
    inputFile = open(filePath, "r")
    return logParse(inputFile.read())


temp = input("enter file path\n")
outputFile = open(temp+".JSON", "w")
outputFile.write(fileInput(temp))
