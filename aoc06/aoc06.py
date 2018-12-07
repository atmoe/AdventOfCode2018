#!/usr/bin/python

import sys
import re
import datetime
import string


class Coordinate:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

def manhattanDistance(c0, c1):
    return abs(c0.x - c1.x) + abs(c0.y - c1.y)

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

minX = 1000000
minY = 1000000
maxX = -1
maxY = -1
coords = []
for line in inputFile.readlines():
    regexStr = "^(\d+), (\d+)$"
    m = re.match(regexStr, line)
    assert m, "File line is not a coordinate! line = " + line

    x = int(m.group(1))
    y = int(m.group(2))

    if(x < minX): minX = x
    if(y < minY): minY = y
    if(x > maxX): maxX = x
    if(y > maxY): maxY = y

    coord = Coordinate(x, y, chr(ord('A') + len(coords)))
    coords.append(coord)

inputFile.close()

enablePrintCoords = True
if enablePrintCoords:
    for c in coords:
        print c.name + " (" + str(c.x) + ", " + str(c.y) + ")"

print "Grid Extent = (" + str(minX) + ", " + str(minY) + ") -> (" + str(maxX) + ", " + str(maxY) + ")"

grid = [["o" for x in range(maxX+1)] for y in range(maxY+1)]

enableGridPrint = True
if enableGridPrint: 
    for g in grid:
        print g
    print "--------------------------------------"

for y in range(maxY+1):
    for x in range(maxX+1):
        gridCoord = Coordinate(x,y, "n/a")

        coordDist = []
        minDist = 10000000
        minCoord = Coordinate(-1,-1,"n/a")
        multipleMin = False
        for coord in coords:
            dist = manhattanDistance(gridCoord, coord)
            if(dist < minDist):
                minDist = dist
                minCoord = coord
            elif(dist==minDist):
                minCoord = Coordinate(-1, -1, ".")

        grid[y][x] = minCoord.name

if enableGridPrint: 
    for g in grid:
        print g
