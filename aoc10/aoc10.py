#!/usr/bin/python

import sys
import re
import datetime
import string
import copy

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, vec):
        self.x += vec.x
        self.y += vec.y

class Light:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position.add(self.velocity)


assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

lights = []
minX = 100000
minY = 100000
maxX = -100000
maxY = -100000
inputFile = open(sys.argv[1], "r")

for line in inputFile.readlines():
    m = re.match("^position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>$", line)
    assert m, "unexpected input! line = \'" + line + "\'"

    pos = Vector(int(m.group(1)), int(m.group(2)))
    vel = Vector(int(m.group(3)), int(m.group(4)))
    newLight = Light(pos, vel)
    lights.append(newLight)

    if(pos.x < minX): minX = pos.x
    if(pos.y < minY): minY = pos.y
    if(pos.x > maxX): maxX = pos.x
    if(pos.y > maxY): maxY = pos.y

inputFile.close()

origin = Vector(minX, minY)

print "#Lights = ",
print "grid = ", (maxX-minX+1), "x", (maxY-minY+1)
print "(", minX, ", ", minY, ") -> (", maxX, ", ", maxY, ")"


update = True
second = 0

while second < 50000:
    minX =  1000000
    minY =  1000000
    maxX = -1000000
    maxY = -1000000
    for l in lights:
        if(l.position.x < minX): minX = l.position.x
        if(l.position.y < minY): minY = l.position.y
        if(l.position.x > maxX): maxX = l.position.x
        if(l.position.y > maxY): maxY = l.position.y
  
    threshold = 100
    xRange = maxX - minX + 1
    yRange = maxY - minY + 1
    if (xRange <= threshold) and (yRange <= threshold):
        print "----------------------------------------------------"
        print "second = ", second, " => ", xRange, "x", yRange
        print "----------------------------------------------------"

        gridSizeX = maxX-minX+1
        gridSizeY = maxY-minY+1

        grid = [["." for x in range(gridSizeX)] for y in range(gridSizeY)]
        for l in lights:
            xLoc = l.position.x - minX
            yLoc = l.position.y - minY 
            grid[yLoc][xLoc] = "#"
        for g in grid:
            print ''.join(g)

    for l in lights: l.update()
 
    second += 1





