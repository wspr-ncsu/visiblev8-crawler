import io
import json


class Script:
    numGets = 0
    gets = {}
    numFunc = 0
    functionCalls = {}
    numObj = 0
    objects = {}
    numSets = 0
    sets = {}
    numChildren = 0
    children = {}
    numOrigins = 0
    windowOrigins = {}

    def __init__(self, i):
        self.scriptNum = i

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)


def searchTree(root: Script, target: int):
    if root.numChildren == 0:
        return 0
    elif root.scriptNum == target:
        return root
    else:
        for child in root.children:
            result = searchTree(root.children[child], target)
            if result != 0:
                return result


def logParse(logString):
    root: Script = Script(0)
    currentLevel: Script = root
    logIterator = io.StringIO(logString)
    for line in logIterator:
        if line[0] == 'g':
            currentLevel.gets[currentLevel.numGets] = line[1:]
            currentLevel.numGets += 1

        elif line[0] == 'n':
            currentLevel.objects[currentLevel.numObj] = line[1:]
            currentLevel.numObj += 1

        elif line[0] == 's':
            currentLevel.sets[currentLevel.numSets] = line[1:]
            currentLevel.numSets += 1

        elif line[0] == 'c':
            currentLevel.functionCalls[currentLevel.numFunc] = line[1:]
            currentLevel.numFunc += 1

        elif line[0] == '$':
            script = 0
            i = 1
            while line[i] != ':':
                i += 1
            try:
                idNumber = int(line[1:i])
            except ValueError:
                idNumber = -1
            newScript = Script(idNumber)
            currentLevel.children[currentLevel.numChildren] = newScript
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
            currentLevel.windowOrigins[currentLevel.numOrigins] = line[2:line.__len__() - 1]
            currentLevel.numOrigins += 1

    print(root.toJSON())


def fileInput(filePath):
    inputFile = open(filePath, "r")
    return logParse(inputFile.read())


temp = input("enter file path\n")
fileInput(temp)
