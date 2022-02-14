import io
import json


class Script:
    def __init__(self, i, text):
        self.scriptNum = i
        self.scriptText = text
        self.numGets = 0
        self.gets = []
        self.numFunc = 0
        self.functionCalls = []
        self.numObj = 0
        self.objects = []
        self.numSets = 0
        self.sets = []
        self.numChildren = 0
        self.children = []
        self.numOrigins = 0
        self.windowOrigins = []

    def _toJSON(self):
        return {
            'scriptNum': self.scriptNum,
            'numGets': self.numGets,
            'gets': self.gets,
            'numFunc': self.numFunc,
            'functionCalls': self.functionCalls,
            'numObj': self.numObj,
            'objects': self.objects,
            'numSets': self.numSets,
            'sets': self.sets,
            'numChildren': self.numChildren,
            'children': [x._toJSON() for x in self.children],
            'numOrigins': self.numOrigins,
            'windowOrigins': self.windowOrigins,
            'scriptText': self.scriptText
        }

    def toJSON(self):
        return json.dumps(self._toJSON())


def searchTree(root: Script, target: int):
    if root.numChildren == 0:
        return 0
    elif root.scriptNum == target:
        return root
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
            currentLevel.gets.append(line[1:line.__len__()-1])
            currentLevel.numGets += 1

        elif line[0] == 'n':
            currentLevel.objects.append(line[1:line.__len__()-1])
            currentLevel.numObj += 1

        elif line[0] == 's':
            currentLevel.sets.append(line[1:line.__len__()-1])
            currentLevel.numSets += 1

        elif line[0] == 'c':
            currentLevel.functionCalls.append(line[1:line.__len__()-1])
            currentLevel.numFunc += 1

        elif line[0] == '$':
            i = 1
            while line[i] != ':':
                i += 1
            try:
                idNumber = int(line[1:i])
            except ValueError:
                idNumber = -1
            newScript = Script(idNumber, line[i+1:line.__len__()-1])
            currentLevel.children.append(newScript)
            currentLevel.numChildren += 1

        elif line[0] == '!':
            try:
                idNumber = int(line[1:])
            except ValueError:
                idNumber = -1
            result = searchTree(root, idNumber)
            if type(result) == type(Script):
                currentLevel = result

        elif line[0] == '@':
            currentLevel.windowOrigins.append(line[2:line.__len__() - 2])
            currentLevel.numOrigins += 1

    return root.toJSON()


def fileInput(filePath):
    inputFile = open(filePath, "r")
    return logParse(inputFile.read())


temp = input("enter file path\n")
outputFile = open(temp+".JSON", "w")
outputFile.write(fileInput(temp))
