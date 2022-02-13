import io

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
    root = Script(0)
    currentLevel = root
    logIterator = io.StringIO(logString)
    for line in logIterator:
        if line[0] == 'g':
            currentLevel.gets[currentLevel.numGets] = line[2:]
            currentLevel.numGets += 1

        elif line[0] == 'n':
            currentLevel.objects[currentLevel.numObj] = line[2:]
            currentLevel.numObj += 1

        elif line[0] == 's':
            currentLevel.sets[currentLevel.numSets] = line[2:]
            currentLevel.numSets += 1

        elif line[0] == 'c':
            currentLevel.functionCalls[currentLevel.numFunc] = line[2:]
            currentLevel.numFunc += 1

        elif line[0] == '$':
            script = 0
            i = 1
            while line[i] != ':':
                i += 1
            idNumber = int(line[1:i])
            newScript = Script(idNumber)
            currentLevel.children[currentLevel.numChildren] = newScript
            currentLevel.numChildren += 1

        elif line[0] == '!':
            idNumber = int(line[1:])
            result = searchTree(root, idNumber)
            if result != 0:
                currentLevel = result

        elif line[0] == '@':
            currentLevel.windowOrigins[currentLevel.numOrigins] = line[2:line.__len__() - 1]
            currentLevel.numOrigins += 1


def fileInput(filePath):
    inputFile = open(filePath, "r")
    return logParse(inputFile.read())


temp = input("enter file path\n")
print(fileInput(temp))
