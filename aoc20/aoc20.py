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

def mapToGrid(loc, gridRoot):
    return Location(loc.x-gridRoot.x, loc.y-gridRoot.y)

def printGrid(grid, w, h):
    print "---------------------"
    print "--- {} x {}".format(w, h)
    print "---------------------"
    # add border
    gridToPrint = copy.deepcopy(grid)
    for g in gridToPrint:
        g.append("#")
        g.insert(0,"#")
    gridToPrint.append("#"*len(gridToPrint[0]))
    gridToPrint.insert(0,"#"*len(gridToPrint[0]))

    for g in gridToPrint:
        print "".join(g)

    print

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

#################
#### Controls ###
#################
enPrintRegex = True
enPrintGrid  = True

inputFile = open(sys.argv[1], "r")
regex = inputFile.readline().strip()
inputFile.close()

regex = regex[1:-1] # strip $ and ^

if enPrintRegex:
    print regex 

# Collect Locations
roomLocs = []
doorLocs = []
locStack = []
currLoc = Location(0,0)
for i in range(len(regex)):

    if regex[i] == "N":
        doorLocs.append(Location(currLoc.x, currLoc.y-1))
        roomLocs.append(Location(currLoc.x, currLoc.y-2))
        currLoc.y-=2
    elif regex[i] == "S":
        doorLocs.append(Location(currLoc.x, currLoc.y+1))
        roomLocs.append(Location(currLoc.x, currLoc.y+2))
        currLoc.y+=2
    elif regex[i] == "E":
        doorLocs.append(Location(currLoc.x+1, currLoc.y))
        roomLocs.append(Location(currLoc.x+2, currLoc.y))
        currLoc.x+=2
    elif regex[i] == "W":
        doorLocs.append(Location(currLoc.x-1, currLoc.y))
        roomLocs.append(Location(currLoc.x-2, currLoc.y))
        currLoc.x-=2
    elif regex[i] == "(":
        locStack.append(Location(currLoc.x, currLoc.y))
    elif regex[i] == "|":
        currLoc = Location(locStack[-1].x, locStack[-1].y)
    elif regex[i] == ")":
        locStack.pop()


# Construct grid
minX =  100000000
minY =  100000000
maxX = -100000000
maxY = -100000000
for l in roomLocs:
    if l.x < minX: minX = l.x
    if l.x > maxX: maxX = l.x
    if l.y < minY: minY = l.y
    if l.y > maxY: maxY = l.y

width  = maxX-minX+1
height = maxY-minY+1
grid = [["#" for x in range(width)] for y in range(height)]

gridLoc = mapToGrid(Location(0,0), Location(minX, minY))
grid[gridLoc.y][gridLoc.x] = "X"

for l in roomLocs:
    gridLoc = mapToGrid(l, Location(minX, minY))
    grid[gridLoc.y][gridLoc.x] = "."
for l in doorLocs:
    gridLoc = mapToGrid(l, Location(minX, minY))
    character = "|" if l.y%2 == 0 else "-"
    grid[gridLoc.y][gridLoc.x] = character

if enPrintGrid: printGrid(grid, width, height)

# Determine distances
dist = 0
currLocs = []
currLocs.append(mapToGrid(Location(0,0),Location(minX, minY)))
distGrid = copy.deepcopy(grid)
while currLocs:
    nextLocs = []
    for l in currLocs:
        distGrid[l.y][l.x] = str(dist)

        upFree    = l.y != 0        and distGrid[l.y-1][l.x] == "-" and distGrid[l.y-2][l.x] == "."
        downFree  = l.y != width-1  and distGrid[l.y+1][l.x] == "-" and distGrid[l.y+2][l.x] == "."
        leftFree  = l.x != 0        and distGrid[l.y][l.x-1] == "|" and distGrid[l.y][l.x-2] == "."
        rightFree = l.x != height-1 and distGrid[l.y][l.x+1] == "|" and distGrid[l.y][l.x+2] == "."

        if upFree:    nextLocs.append(Location(l.x, l.y-2))
        if downFree:  nextLocs.append(Location(l.x, l.y+2))
        if leftFree:  nextLocs.append(Location(l.x-2, l.y))
        if rightFree: nextLocs.append(Location(l.x+2, l.y))

    dist+=1
    del currLocs[:]
    for l in nextLocs:
        currLocs.append(l)
    del nextLocs[:]

if enPrintGrid: printGrid(distGrid, width, height)

# Find Max
print "Max distance = {}".format(dist-1)

gt1000 = 0
for y in range(len(distGrid)):
    for x in range(len(distGrid[0])):
        if distGrid[y][x] == "#": continue
        if distGrid[y][x] == "-": continue
        if distGrid[y][x] == "|": continue

        if int(distGrid[y][x]) >= 1000: gt1000+=1


print "Greater than 1000 doors = {}".format(gt1000)




