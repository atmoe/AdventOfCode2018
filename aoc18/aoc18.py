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


assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

inputFile = open(sys.argv[1], "r")

initForest = []
for line in inputFile.readlines():
    initForest.append(list(line.strip()))
inputFile.close()

maxX = len(initForest[0])-1
maxY = len(initForest)-1
print "Grid is {}x{}".format(maxX+1, maxY+1)

'''
print "--------------------"
print "---- Initial"
print "--------------------"
for l in initForest:
    print "".join(l)
for m in range(1,11):
    nextForest = [["" for x in range(maxX+1)] for y in range(maxY+1)]
    print "--------------------"
    print "---- Minute {}".format(m)
    print "--------------------"

    for y in range(maxY+1):
        for x in range(maxX+1):
            n  = "." if            y==0    else forest[y-1][x]
            ne = "." if x==maxX or y==0    else forest[y-1][x+1]
            e  = "." if x==maxX            else forest[y][x+1]
            se = "." if x==maxX or y==maxY else forest[y+1][x+1]
            s  = "." if            y==maxY else forest[y+1][x]
            sw = "." if x==0    or y==maxY else forest[y+1][x-1]
            w  = "." if x==0               else forest[y][x-1]
            nw = "." if x==0    or y==0    else forest[y-1][x-1]

            vals = [n, ne, e, se, s, sw, w, nw]

            openSum  = vals.count(".")
            treesSum = vals.count("|")
            yardSum  = vals.count("#")

            assert (openSum+treesSum+yardSum) == 8, "didnt sum to 8!"
            if forest[y][x] == ".":
                if treesSum >= 3: nextForest[y][x] = "|"
                else:             nextForest[y][x] = "."
            elif forest[y][x] == "|":
                if yardSum >= 3:  nextForest[y][x] = "#"
                else:             nextForest[y][x] = "|"
            elif forest[y][x] == "#":
                if yardSum >= 1 and treesSum >= 1: nextForest[y][x] = "#"
                else:                              nextForest[y][x] = "."

    forest = copy.deepcopy(nextForest)
    trees       = 0
    lumberyards = 0
    for l in forest:
        trees      +=l.count("|")
        lumberyards+=l.count("#")
        print "".join(l)
    print "Resource Value = {}".format(trees*lumberyards)
'''

for l in initForest:
    l.append(".")
    l.insert(0,".")

initForest.append("."*len(initForest[0]))
initForest.insert(0,"."*len(initForest[0]))

print "--------------------"
print "---- Initial"
print "--------------------"
for l in initForest:
    print "".join(l)

forest0 = copy.deepcopy(initForest)
forest1 = copy.deepcopy(initForest)

forestAtMinute = []
forestAtMinute.append(initForest)

minutes = 1000
firstRepeatFound = False
firstRepeatMinute = 0
repeatLength = 0
for m in range(1,minutes+1):
    if m % 2 == 1: 
        thisForest = forest0
        nextForest = forest1
    else:
        nextForest = forest0
        thisForest = forest1

    if m % 1000 == 0:
        print "---- Minute {}".format(m) 

    for y in range(1,maxY+2):
        for x in range(1,maxX+2):
            treeSum  = thisForest[y-1][x-1:x+2].count("|") + thisForest[y][x-1].count("|") + thisForest[y][x+1].count("|") + thisForest[y+1][x-1:x+2].count("|")
            yardSum  = thisForest[y-1][x-1:x+2].count("#") + thisForest[y][x-1].count("#") + thisForest[y][x+1].count("#") + thisForest[y+1][x-1:x+2].count("#")

            if thisForest[y][x] == ".":
                if treeSum >= 3: nextForest[y][x] = "|"
                else:            nextForest[y][x] = "."
            elif thisForest[y][x] == "|":
                if yardSum >= 3:  nextForest[y][x] = "#"
                else:             nextForest[y][x] = "|"
            elif thisForest[y][x] == "#":
                if yardSum >= 1 and treeSum >= 1: nextForest[y][x] = "#"
                else:                             nextForest[y][x] = "."

    for pastMin, f in enumerate(forestAtMinute):
        if f == nextForest:
            if not firstRepeatFound:
                firstRepeatMinute=pastMin
                firstRepeatFound=True
                repeatLength=m-pastMin
            print "Minute {} same as minute {}".format(m, pastMin)

    forestAtMinute.append(copy.deepcopy(nextForest))


    #print "--------------------"
    #print "---- Minute {}".format(m)
    #print "--------------------"
    #for l in nextForest:
    #    print "".join(l)

    if firstRepeatFound: 
        forestToAnalyze = forestAtMinute[((1000000000-firstRepeatMinute)%repeatLength)+firstRepeatMinute]
        break

print "--------------------"
print "---- Final "
print "--------------------"
trees       = 0
lumberyards = 0
for l in forestToAnalyze:
    trees      +=l.count("|")
    lumberyards+=l.count("#")
    print "".join(l)
print "Resource Value at 1,000,000,000 = {}".format(trees*lumberyards)



