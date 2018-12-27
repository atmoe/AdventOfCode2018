#!/usr/bin/python

import sys
import re
import datetime
import string
import copy
import random


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getStr(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

class GraphVert:
    def __init__(self,x,y,t):
        self.x     = x
        self.y     = y
        self.tool  = t
        self.dist  = 1000000000

    def updateCost(self, newDist):
        if newDist < self.dist: 
            self.dist  = newDist

def getToolIdx(tool):
    if tool == "t": return 0
    if tool == "c": return 1
    if tool == "n": return 2

def toolWorksOn(tool,rtype):
    if tool == "t" and rtype==0: return True
    if tool == "t" and rtype==2: return True
    if tool == "c" and rtype==0: return True
    if tool == "c" and rtype==1: return True
    if tool == "n" and rtype==1: return True
    if tool == "n" and rtype==2: return True
    return False

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

inputFile = open(sys.argv[1], "r")
d = re.match("^depth: (\d+)$", inputFile.readline())
t = re.match("^target: (\d+),(\d+)$", inputFile.readline())
depth  = int(d.group(1))
target = Location(int(t.group(1)), int(t.group(2)))
inputFile.close()

print "depth = {}".format(depth)
print "target = {}".format(target.getStr())

gridBloat = 1000

gridWidth  = target.x+1 + gridBloat
gridHeight = target.y+1 + gridBloat
geologicIdx = [[-1 for x in range(gridWidth)] for y in range(gridHeight)]
erosionLvl  = [[-1 for x in range(gridWidth)] for y in range(gridHeight)]
regionType  = [[-1 for x in range(gridWidth)] for y in range(gridHeight)]
for y in range(gridHeight):
    for x in range(gridWidth):
        if x == 0 and y ==0:
            geologicIdx[y][x] = 0
        elif x == target.x and y == target.y:
            geologicIdx[y][x] = 0
        elif y == 0:
            geologicIdx[y][x] = x * 16807
        elif x == 0:
            geologicIdx[y][x] = y * 48271
        else:
            geologicIdx[y][x] = erosionLvl[y][x-1] * erosionLvl[y-1][x]
            assert erosionLvl[y][x-1] >= 0, "incorrect erosion level at {},{} = {}".format(y, x-1, erosionLvl[y][x-1])
            assert erosionLvl[y-1][x] >= 0, "incorrect erosion level at {},{} = {}".format(y, x-1, erosionLvl[y-1][x])

        erosionLvl[y][x] = (geologicIdx[y][x] + depth) % 20183
        regionType[y][x] = erosionLvl[y][x] % 3

printGrid = False
if printGrid:
    for y in range(gridHeight):
        for x in range(gridWidth):
            rType = regionType[y][x]
            if x==0 and y==0:                 sys.stdout.write("M")
            elif x==target.x and y==target.y: sys.stdout.write("T")
            elif rType == 0:                  sys.stdout.write(".")
            elif rType == 1:                  sys.stdout.write("=")
            elif rType == 2:                  sys.stdout.write("|")
        sys.stdout.write("\n") 
        sys.stdout.flush()

totalRisk = 0
for y in range(target.y+1):
    for x in range(target.x+1):
        totalRisk += regionType[y][x]

print "totalRisk = {}".format(totalRisk)

graph = [[[GraphVert(0,0,0) for x in range(gridWidth)] for y in range(gridHeight)] for z in range(3)]
for y in range(gridHeight):
    for x in range(gridWidth):
        for t in ["t","c","n"]:
            graph[getToolIdx(t)][y][x] = GraphVert(x,y,t)

# tools:
#   t - torch
#   c - climbing gear
#   n - neither
#   inv - invalid
initPoint = graph[0][0][0]
initPoint.dist  = 0

currWidth  = 1
currHeight = 1
totalVerts = gridWidth * gridHeight
vertNum    = 0
vertsNotAtMin = True
vertPool = []
vertPool.append(initPoint)
while vertsNotAtMin:

    # find min vert
    minDist = 1000000000
    minVert = None
    for v in vertPool:
        if v.dist < minDist:
            minDist = v.dist
            minVert = v

    if minVert.x+1 > currWidth:  currWidth  = minVert.x + 1
    if minVert.y+1 > currHeight: currHeight = minVert.y + 1

    vertPool.remove(minVert)

    assert minVert.y+1 < gridHeight, "grid not tall enough, minVert at ({},{})".format(minVert.x, minVert.y)
    assert minVert.x+1 < gridWidth,  "grid not wide enough, minVert at ({},{})".format(minVert.x, minVert.y)

    if vertNum%1000==0: 
        print "Vert {0} pos=({1:4},{2:4}) dist = {3}".format(vertNum, minVert.x, minVert.y, minVert.dist)

    #### Find Legal Edges
    edges = []

    # Tool Swaps
    if regionType[minVert.y][minVert.x] == 0: # rocky
        if   minVert.tool=="t": edges.append(graph[getToolIdx("c")][minVert.y][minVert.x])
        elif minVert.tool=="c": edges.append(graph[getToolIdx("t")][minVert.y][minVert.x])
        else: assert 0, ""
    elif regionType[minVert.y][minVert.x] == 1: # wet
        if   minVert.tool=="c": edges.append(graph[getToolIdx("n")][minVert.y][minVert.x])
        elif minVert.tool=="n": edges.append(graph[getToolIdx("c")][minVert.y][minVert.x])
        else: assert 0, ""
    elif regionType[minVert.y][minVert.x] == 2: # narrow
        if   minVert.tool=="t": edges.append(graph[getToolIdx("n")][minVert.y][minVert.x])
        elif minVert.tool=="n": edges.append(graph[getToolIdx("t")][minVert.y][minVert.x])
        else: assert 0, ""

    if minVert.y!=0:
        if toolWorksOn(minVert.tool, regionType[minVert.y-1][minVert.x]):
            edges.append(graph[getToolIdx(minVert.tool)][minVert.y-1][minVert.x])

    if minVert.x!=0:
        if toolWorksOn(minVert.tool, regionType[minVert.y][minVert.x-1]):
            edges.append(graph[getToolIdx(minVert.tool)][minVert.y][minVert.x-1])

    if toolWorksOn(minVert.tool, regionType[minVert.y+1][minVert.x]):
        edges.append(graph[getToolIdx(minVert.tool)][minVert.y+1][minVert.x])

    if toolWorksOn(minVert.tool, regionType[minVert.y][minVert.x+1]):
        edges.append(graph[getToolIdx(minVert.tool)][minVert.y][minVert.x+1])

    for e in edges:
        if e.dist == 1000000000:
            # first time visiting this vert, add to pool
            vertPool.append(e)

        if e.tool != minVert.tool:
            e.updateCost(minVert.dist+7)
        else:
            e.updateCost(minVert.dist+1)

    # check if all min
    vertsNotAtMin = len(vertPool) > 0

    vertNum+=1

    if minVert.x == target.x and minVert.y == target.y and minVert.tool=="t":
        print "At end!"
        vertsNotAtMin = False

print "---------------"
print "Min Vert Dist = {}".format(minVert.dist)

