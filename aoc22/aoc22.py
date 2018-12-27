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

