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
        elif newDist == self.dist:
            for t in tools:
                if not t in self.tools:
                    self.tools.append(t)

    # rType 0 - rock
    # rType 1 - wet
    # rType 2 - narrow
    def costToNeighbor(self, neighborRType):
        #print "sT = {}, nT = {}".format(self.rType, neighborRType)
        # Check for 1-cost
        if neighborRType == self.rType:
            return 1 # same type

        if neighborRType==0:
            if   "t" in self.tools: return 1 # torch    is 1 to go to rocky
            elif "c" in self.tools: return 1 # climbing is 1 to go to rocky
            else:                   return 8 # must switch away from neither

        elif neighborRType==1:
            if   "c" in self.tools: return 1 # climbing is 1 to go to wet
            elif "n" in self.tools: return 1 # neither  is 1 to go to wet
            else:                   return 8 # must switch away from torch

        elif neighborRType==2:
            if   "t" in self.tools: return 1 # torch   is 1 to go to narrow
            elif "n" in self.tools: return 1 # neither is 1 to go to narrow
            else:                   return 8 # must switch away from climbing

        assert 0, "no cost found!"

    def toolsToN(self, neighborRType):
        # Check for 1-cost
        newTools = []
        if neighborRType == self.rType:
            for t in self.tools:
                newTools.append(t)
            return newTools

        if neighborRType==0:
            if "t" in self.tools:
                newTools.append("t")
            if "c" in self.tools:
                newTools.append("c")

            if not "t" in self.tools and not "c" in self.tools and "n" in self.tools:
                # no neither rock, had to switch, two options
                newTools.append("c")
                newTools.append("t")

        elif neighborRType==1:
            if "n" in self.tools:
                newTools.append("n")
            if "c" in self.tools:
                newTools.append("c")

            if not "n" in self.tools and not "c" in self.tools and "t" in self.tools:
                # no wet torch, had to switch, two options
                newTools.append("n")
                newTools.append("c")

        elif neighborRType==2:
            if "t" in self.tools:
                newTools.append("t")
            if "n" in self.tools:
                newTools.append("n")

            if not "t" in self.tools and not "n" in self.tools and "c" in self.tools:
                # no narrow climbing, had to switch, two options
                newTools.append("t")
                newTools.append("n")

        return newTools

        assert 0, "no tools found! currentTools = {} {}"

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

graph = [[GraphVert(0,0,0) for x in range(gridWidth)] for y in range(gridHeight)]
for y in range(gridHeight):
    for x in range(gridWidth):
        graph[y][x] = GraphVert(x,y,regionType[y][x])

# tools:
#   t - torch
#   c - climbing gear
#   n - neither
#   inv - invalid
graph[0][0].dist = 0
graph[0][0].tools = ["t"]
graph[0][0].atMin = False

currWidth  = 1
currHeight = 1
totalVerts = gridWidth * gridHeight
vertNum = 0
vertsNotAtMin = True
vertPool = []
vertPool.append(graph[0][0])
while vertsNotAtMin:

    # find min vert
    minDist = 1000000000
    minVert = None
    for v in vertPool:
        if v.dist < minDist and not v.atMin:
            minDist = v.dist
            minVert = v

    minVert.atMin = True
    if minVert.x+1 > currWidth:  currWidth  = minVert.x + 1
    if minVert.y+1 > currHeight: currHeight = minVert.y + 1
    vertPool.remove(minVert)
    assert minVert.y+1 < gridHeight, "grid not tall enough, minVert at ({},{})".format(minVert.x, minVert.y)
    assert minVert.x+1 < gridWidth,  "grid not wide enough, minVert at ({},{})".format(minVert.x, minVert.y)

    if vertNum%1000==0: 
        print "Vert {0} ({1:.3}%) pos=({2},{3}) dist = {4}".format(vertNum, vertNum/float(totalVerts)*100, minVert.x, minVert.y, minVert.dist)

    #### update neighbors
    nVerts = []
    if minVert.y!=0:
        nVerts.append(graph[minVert.y-1][minVert.x]) # up
    if minVert.x!=0:
        nVerts.append(graph[minVert.y][minVert.x-1]) # left
    nVerts.append(graph[minVert.y+1][minVert.x]) # down
    nVerts.append(graph[minVert.y][minVert.x+1]) # right

    for idx,v in enumerate(nVerts):
        if v.dist == 1000000000:
            # first time visiting this vert, add to pool
            vertPool.append(v)

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

    if printGrid:
        print "---------------"
        for row in range(currHeight+2):
            for col in range(currWidth+2):
                v = graph[row][col]
                if v.atMin==True: minStr = "*"
                else:             minStr = " "
                if minVert==v:
                    print "xx {0:4} xxx".format(minVert.dist),
                else:
                    print "{0:10}{1}".format(v.dist,minStr),
            print

        a = raw_input()


print "---------------"
print "Min Vert Dist = {}".format(minVert.dist)

