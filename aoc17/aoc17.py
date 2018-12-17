#!/usr/bin/python

import sys
import re
import datetime
import string
import copy
import random


def gridLoc(loc, root):
    return Location(loc.x-root.x, loc.y-root.y)

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


assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

inputFile = open(sys.argv[1], "r")

clayLocations = []
for line in inputFile.readlines():
    xFirst = re.match("^x=(\d+), y=(\d+)\.\.(\d+)$", line)
    yFirst = re.match("^y=(\d+), x=(\d+)\.\.(\d+)$", line)

    assert xFirst or yFirst, "line doesnt match expectations! line = " + line

    if yFirst: 
        y      = int(yFirst.group(1))
        xStart = int(yFirst.group(2))
        xEnd   = int(yFirst.group(3))
        for x in range(xStart, xEnd+1):
            clayLocations.append(Location(x, y))

    elif xFirst:
        x      = int(xFirst.group(1))
        yStart = int(xFirst.group(2))
        yEnd   = int(xFirst.group(3))
        for y in range(yStart, yEnd+1):
            clayLocations.append(Location(x, y))
inputFile.close()

## Construct Grid
minX = 500
maxX = 500
minY = 100 
maxY = 0
for cl in clayLocations:
    if cl.x > maxX: maxX=cl.x
    if cl.x < minX: minX=cl.x
    if cl.y > maxY: maxY=cl.y
    if cl.y < minY: minY=cl.y

# expand by one either direction inX to account for water flow (if needed)
maxX += 1
minX -= 1
gridWidth  = maxX - minX + 1
gridHeight = maxY + 1
gridTopLeft = Location(minX, 0)

print "Grid Setup:"
print " -- {} x {}".format(gridWidth, gridHeight)
print " -- ({}, {}) -> ({}, {})".format(minX, 0, maxX, maxY)

grid = [["." for x in range(gridWidth)] for y in range(gridHeight)]

# Add Spring
springLoc     = Location(500, 0)
springLocGrid = gridLoc(springLoc,gridTopLeft)
grid[springLocGrid.y][springLocGrid.x] = "+"

for cl in clayLocations:
    clayLocGrid = gridLoc(cl, gridTopLeft)
    grid[clayLocGrid.y][clayLocGrid.x] = "#"

for g in grid:
    print "".join(g)


# while source exists
#   move down if possible
#       cant move down due to clay or due to other water
#   if cannot move down check spread in both directions:
#       move both left and right until can drop or blocked
#       1) blocked in both directions
#           - mark all as filled: ~
#       2) blocked in one or neither
#           - mark all as moving: |
#           - non blocked (1 or two) added to source list

tick = 0
sources = []
sources.append(Location(springLoc.x, springLoc.y+1))
while sources:
    print "----------------"
    print "--- Tick {}".format(tick)
    print "----------------"
    currSource = sources.pop()
    currSourceGridLoc = gridLoc(currSource, gridTopLeft)
    grid[currSourceGridLoc.y][currSourceGridLoc.x] = "|"

    if currSource.y != maxY:

        aboveSand  = grid[currSourceGridLoc.y+1][currSourceGridLoc.x] == "."
        aboveWater = grid[currSourceGridLoc.y+1][currSourceGridLoc.x] == "~"
        aboveFlow  = grid[currSourceGridLoc.y+1][currSourceGridLoc.x] == "|"
        # Check if hitting water, if so die
   
        if aboveSand:
            sources.append(Location(currSource.x, currSource.y+1)) 
        elif not aboveFlow:
            # works correctly if above water or above clay

            # walk left
            leftSteps = 0
            leftNewSource = False
            leftWallHit   = False
            while not leftNewSource and not leftWallHit:
                leftSteps+=1
                leftIsClay       = grid[currSourceGridLoc.y][currSourceGridLoc.x-leftSteps] == "#"
                leftIsSand       = grid[currSourceGridLoc.y][currSourceGridLoc.x-leftSteps] == "."
                leftIsAboveClay  = grid[currSourceGridLoc.y+1][currSourceGridLoc.x-leftSteps] == "#"
                leftIsAboveWater = grid[currSourceGridLoc.y+1][currSourceGridLoc.x-leftSteps] == "~"
                leftIsAboveSand  = grid[currSourceGridLoc.y+1][currSourceGridLoc.x-leftSteps] == "."
                leftIsAboveFlow  = grid[currSourceGridLoc.y+1][currSourceGridLoc.x-leftSteps] == "|"

                leftWallHit   = leftIsClay
                leftNewSource = not leftWallHit and not leftIsAboveClay and not leftIsAboveWater
                if leftWallHit: leftSteps-=1

            rightSteps = 0
            rightNewSource = False
            rightWallHit   = False
            while not rightNewSource and not rightWallHit:
                rightSteps+=1
                rightIsClay       = grid[currSourceGridLoc.y][currSourceGridLoc.x+rightSteps] == "#"
                rightIsSand       = grid[currSourceGridLoc.y][currSourceGridLoc.x+rightSteps] == "."
                rightIsAboveClay  = grid[currSourceGridLoc.y+1][currSourceGridLoc.x+rightSteps] == "#"
                rightIsAboveWater = grid[currSourceGridLoc.y+1][currSourceGridLoc.x+rightSteps] == "~"
                rightIsAboveSand  = grid[currSourceGridLoc.y+1][currSourceGridLoc.x+rightSteps] == "."
                rightIsAboveFlow  = grid[currSourceGridLoc.y+1][currSourceGridLoc.x+rightSteps] == "|"
    
                rightWallHit   = rightIsClay
                rightNewSource = not rightWallHit and not rightIsAboveClay and not rightIsAboveWater
                if rightWallHit: rightSteps-=1
       

            for x in range(currSourceGridLoc.x-leftSteps, currSourceGridLoc.x+rightSteps+1):
                if leftWallHit and rightWallHit:
                    grid[currSourceGridLoc.y][x] = "~"
                else:
                    grid[currSourceGridLoc.y][x] = "|"

            if leftWallHit and rightWallHit:
                sources.append(Location(currSource.x, currSource.y-1))

            else:
                if leftNewSource:  sources.append(Location(currSource.x-leftSteps, currSource.y))
                if rightNewSource: sources.append(Location(currSource.x+rightSteps, currSource.y))

    tick += 1

for g in grid:
    print "".join(g)

waterCount = 0
notDrainedWaterCount = 0
for y in range(len(grid)):
    if y < minY: continue
    for x in grid[y]:
        if x == "|" or x == "~": waterCount+=1
        if x == "~": notDrainedWaterCount+=1

print "Total Water Count = {}".format(waterCount)
print "Total Water Count (not drained) = {}".format(notDrainedWaterCount)

