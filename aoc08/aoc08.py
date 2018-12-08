#!/usr/bin/python

import sys
import re
import datetime
import string
import copy

class Node:
    def __init__(self, name, numChildren, numMeta, parent):
        self.name        = name
        self.numChildren = numChildren
        self.numMeta     = numMeta
        self.parent      = parent
        self.meta        = []
        self.children    = []
        self.value       = 0

    def getStr(self):
        nodeStr  = self.name + ": "
        nodeStr += str(self.numChildren) + " children = ["
        for c in self.children:
            nodeStr += c.name
        nodeStr += "]  "
        nodeStr += str(self.numMeta) + " meta = " + str(self.meta)
        return nodeStr



assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

inputFile = open(sys.argv[1], "r")
lines = inputFile.readlines()
inputFile.close()
assert len(lines) == 1, "File not one line!"

license = list(map(int,lines[0].split()))

#print license

currentName = "A"
root = Node(currentName, license.pop(0), license.pop(0), None)
currentName = str(chr(ord(currentName) + 1))


currentNode = root
metaSum = 0

while len(license) != 0:
#    print currentNode.getStr()
    assert currentNode.numChildren >= len(currentNode.children), "Node has more children than expected"
    assert currentNode.numMeta     >= len(currentNode.meta),     "Node has more meta than expected"

    # Next is Header
    if(currentNode.numChildren > len(currentNode.children)):
        newNode = Node(currentName, license.pop(0), license.pop(0), currentNode)
        currentName = str(chr((ord(currentName) + 1) % 256))
        currentNode.children.append(newNode)
        currentNode = newNode

    # Next is Meta
    elif(currentNode.numChildren == len(currentNode.children)):
        for i in range(currentNode.numMeta):
            currentNode.meta.append(license.pop(0))
            metaSum += currentNode.meta[-1]

        # Calculate Value
        #  - if getting meta, all children have been determined
        print currentNode.getStr()
        if(currentNode.numChildren == 0):
            currentNode.value = sum(currentNode.meta)
        else:
            for m in currentNode.meta:
                if m==0:
                    currentNode.value += 0
                elif m > currentNode.numChildren:
                    currentNode.value += 0
                else:
                    currentNode.value += currentNode.children[m - 1].value


        currentNode = currentNode.parent

print "Sum of all Meta = ", metaSum
print "Value of Root   = ", root.value

