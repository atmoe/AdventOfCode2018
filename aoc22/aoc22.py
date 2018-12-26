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

    def adjacentTo(self, loc):
        above = (self.y+1) == loc.y and self.x == loc.x
        below = (self.y-1) == loc.y and self.x == loc.x
        right = self.y == loc.y and (self.x+1) == loc.x
        left  = self.y == loc.y and (self.x-1) == loc.x
        return above or below or right or left

    # True if location is first in reading order vs point
    def earlierReadingOrderThan(self, point):
        #assert not (self.y==point.y and self.x==point.x), "Points are the same!  loc:(" + str(self.x) + ", " + str(self.y) + ")  point: (" + str(point.x) + ", " + str(point.y) +")"

        above = self.y < point.y
        below = self.y > point.y
        left  = self.x < point.x
        right = self.x > point.x

        return above or (left and not below)

class GraphVert:
    def __init__(self,x,y,rType):
        self.x     = x
        self.y     = y
        self.rType = rType 
        self.dist  = 1000000000
        self.tools = []
        self.atMin = False

    def updateCost(self, newDist, tools):
        if newDist < self.dist: 
            self.dist  = newDist
            self.tools = tools

    # rType 0 - rock
    # rType 1 - wet
    # rType 2 - narrow
    def costToNeighbor(self, neighborRType):
        #print "sT = {}, nT = {}".format(self.rType, neighborRType)
        # Check for 1-cost
        if neighborRType == self.rType:
            return 1 # same type

        if "t" in self.tools:
            if   neighborRType==0: return 1 # torch goes to rocky in 1 min
            elif neighborRType==2: return 1 # torch goes to narrow in 1 min

        if "c" in self.tools:
            if   neighborRType==0: return 1 # climbing goes to rocky in 1 min
            elif neighborRType==1: return 1 # climbing goes to wet in 1 min

        if "n" in self.tools:
            if   neighborRType==1: return 1 # neither goes to wet in 1 min
            elif neighborRType==2: return 1 # neither goes to narrow in 1 min

        # Check for 8-cost
        if   neighborRType==1: return 8 # no wet torch - must change to climbing or neither
        elif neighborRType==2: return 8 # no narrow climbing - cmust change to torch or neither
        elif neighborRType==0: return 8 # no rock neither - must change to climbing or torch

        assert 0, "no cost found!"

    def toolsToN(self, neighborRType):
        # Check for 1-cost
        if neighborRType == self.rType:
            return self.tools

        if "t" in self.tools:
            if   neighborRType==0: return ["t", "inv"] # torch goes to rocky in 1 min
            elif neighborRType==2: return ["t", "inv"] # torch goes to narrow in 1 min

        if "c" in self.tools:
            if   neighborRType==0: return ["c", "inv"] # climbing goes to rocky in 1 min
            elif neighborRType==1: return ["c", "inv"] # climbing goes to wet in 1 min

        if "n" in self.tools:
            if   neighborRType==1: return ["n", "inv"] # neither goes to wet in 1 min
            elif neighborRType==2: return ["n", "inv"] # neither goes to narrow in 1 min

        # Check for 8-cost
        if   neighborRType==1: return ["c", "n"] # no wet torch - must change to climbing or neither
        elif neighborRType==2: return ["t", "n"] # no narrow climbing - cmust change to torch or neither
        elif neighborRType==0: return ["c", "t"] # no rock neither - must change to climbing or torch

        assert 0, "no tools found!"

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

inputFile = open(sys.argv[1], "r")
d = re.match("^depth: (\d+)$", inputFile.readline())
t = re.match("^target: (\d+),(\d+)$", inputFile.readline())
depth  = int(d.group(1))
target = Location(int(t.group(1)), int(t.group(2)))
inputFile.close()

print "depth = {}".format(depth)
print "target = {}".format(target.getStr())

gridWidth  = target.x+1 + 500
gridHeight = target.y+1 + 300
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

graph = [[GraphVert(0,0,0) for x in range(gridWidth)] for y in range(gridHeight)]
vertPool = []
for y in range(gridHeight):
    for x in range(gridWidth):
        graph[y][x] = GraphVert(x,y,regionType[y][x])
        if y <= target.y and x <= target.x:
            vertPool.append(graph[y][x])

# tools:
#   t - torch
#   c - climbing gear
#   n - neither
#   inv - invalid
graph[0][0].dist = 0
graph[0][0].tools = ["t", "inv"]
graph[0][0].atMin = False

currWidth  = target.x+1
currHeight = target.y+1
totalVerts = currWidth * currHeight
vertNum = 0
vertsNotAtMin = True
while vertsNotAtMin:
    #print "---------------"
    if vertNum%100==0: print "Vert {0} ({1:3.2}%) ({2:3.2}%)".format(vertNum, vertNum/float(totalVerts)*100, vertNum/float(gridHeight*gridWidth)*100)
    # find min vert
    minDist = 1000000000
    minVert = None
    for v in vertPool:
        if v.dist < minDist and not v.atMin:
            minDist = v.dist
            minVert = v

    minVert.atMin = True
    vertPool.remove(minVert)
    #assert minVert.y+1 < gridHeight, "grid not tall enough, minVert at ({},{})".format(minVert.x, minVert.y)
    #assert minVert.x+1 < gridWidth,  "grid not wide enough, minVert at ({},{})".format(minVert.x, minVert.y)

    #print "Min type  = {}".format(minVert.rType)
    #print "Min tools = ", " ".join(minVert.tools)

    if minVert.y == currHeight-1:
        for x in range(currWidth):
            vertPool.append(graph[minVert.y+1][x])
        currHeight+=1
        totalVerts += currWidth

    if minVert.x == currWidth-1:
        for y in range(currHeight):
            vertPool.append(graph[y][minVert.x+1])
        currWidth+=1
        totalVerts += currHeight

    #### update neighbors
    nVerts = []
    if minVert.y!=0:
        nVerts.append(graph[minVert.y-1][minVert.x]) # up
        #print "up neighbor type = {}, cost = {}".format(nVerts[-1].rType, minVert.costToNeighbor(nVerts[-1].rType))
    if minVert.x!=0:
        nVerts.append(graph[minVert.y][minVert.x-1]) # left
        #print "left neighbor type = {}, cost = {}".format(nVerts[-1].rType, minVert.costToNeighbor(nVerts[-1].rType))
    nVerts.append(graph[minVert.y+1][minVert.x]) # down
    #print "down neighbor type = {}, cost = {}".format(nVerts[-1].rType, minVert.costToNeighbor(nVerts[-1].rType))
    nVerts.append(graph[minVert.y][minVert.x+1]) # right
    #print "right neighbor type = {}, cost = {}".format(nVerts[-1].rType, minVert.costToNeighbor(nVerts[-1].rType))

    for idx,v in enumerate(nVerts):
        costToV      = minVert.costToNeighbor(v.rType)
        toolsForMove = minVert.toolsToN(v.rType)
        v.updateCost(costToV + minVert.dist, toolsForMove)

    # check if all min
    vertsNotAtMin = totalVerts > (vertNum + 1)

    vertNum+=1

    if minVert.x == target.x and minVert.y == target.y:
        if not "t" in minVert.tools:
            minVert.dist += 7
            vertsNotAtMin = False
'''
    for row in graph:
        for v in row:
            if minVert==v:
                print "xx {0:4} xx".format(minVert.dist),
            else:
                print "{0:10}".format(v.dist),
        print
'''

print "---------------"
print "Min Vert Dist = {}".format(minVert.dist)

