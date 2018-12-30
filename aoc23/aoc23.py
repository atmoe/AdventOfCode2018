#!/usr/bin/python

import sys
import re
import datetime
import string
import copy
import random


class Location:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getStr(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def distTo(self,loc):
        return abs(self.x - loc.x) + abs(self.y - loc.y) + abs(self.z - loc.z)

class NanoBot:
    def __init__(self, loc, radius):
        self.loc = loc
        self.r   = radius

class Box:
    def __init__(self, cornerLoc, w, h, d):
        self.corner = cornerLoc # closest corner to -Inf, -Inf, -Inf
        self.w      = w
        self.h      = h
        self.d      = d
        self.bots   = [] # list of all bots contained by or intersecting this box
        self.vol    = w*h*d

        #self.distOrigin = 
    def addPotentialBot(self, bot):
        closestX = max(self.corner.x, min(bot.loc.x, self.corner.x + self.w - 1))
        closestY = max(self.corner.y, min(bot.loc.y, self.corner.y + self.h - 1))
        closestZ = max(self.corner.z, min(bot.loc.z, self.corner.z + self.d - 1))

        if bot.loc.distTo(Location(closestX,closestY,closestZ)) <= bot.r:
            self.bots.append(bot)

    def getStr(self):
        return "Box @ {}\t{}x{}x{}\t(v={}):\t{} bots".format(self.corner.getStr(), self.w, self.h, self.d, self.vol, len(self.bots))

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

bots = []
minX =  1000000000
minY =  1000000000
minZ =  1000000000
maxX = -1000000000
maxY = -1000000000
maxZ = -1000000000
inputFile = open(sys.argv[1], "r")
for line in inputFile.readlines():
    p = re.match("^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$", line)
    assert p, "invalid bot position.  line = {}".format(line)
    botLoc = Location(int(p.group(1)), int(p.group(2)), int(p.group(3)))
    bots.append(NanoBot(botLoc, int(p.group(4))))

    if botLoc.x > maxX: maxX = botLoc.x
    if botLoc.y > maxY: maxY = botLoc.y
    if botLoc.z > maxZ: maxZ = botLoc.z
    if botLoc.x < minX: minX = botLoc.x
    if botLoc.y < minY: minY = botLoc.y
    if botLoc.z < minZ: minZ = botLoc.z
inputFile.close()
maxLoc = Location(maxX, maxY, maxZ)
minLoc = Location(minX, minY, minZ)

bots.sort(key=lambda c: c.r, reverse=True)
strongestBot = bots[0]
weakestBot   = bots[-1]

botsInRange = 0
for b in bots:
    dist = b.loc.distTo(strongestBot.loc)

    if dist <= strongestBot.r:
        botsInRange += 1

print "Bounding Box = {} -> {}".format(minLoc.getStr(), maxLoc.getStr())
print "Bots In Range of Strongest = {}".format(botsInRange)
print "Strongest Bot = {} r = {}".format(strongestBot.loc.getStr(), strongestBot.r)
print "Weakest Bot = {} r = {}".format(weakestBot.loc.getStr(), weakestBot.r)
print "Total Bots = {}".format(len(bots))

initBox = Box(minLoc, maxLoc.x - minLoc.x + 1, maxLoc.y - minLoc.y + 1, maxLoc.z - minLoc.z + 1)
for b in bots:
    initBox.addPotentialBot(b)

print initBox.getStr()

boxes = []
boxes.append(initBox)

iteration=0
foundOneVolBox = False
while not foundOneVolBox:

    maxBots = 0
    maxVol  = 10000000000000000000000000000000000000
    currBox = None
    currBoxIdx = 0
    for idx,b in enumerate(boxes):
        if len(b.bots) > maxBots:
            currBox = b
            currBoxIdx = idx
            maxBots = len(b.bots)

    if currBox.vol == 1:
        foundOneVolBox = True
        break

    del boxes[currBoxIdx]

    if iteration%10==0: 
        print "iter {}: ".format(iteration)
        print "    subVols = {}".format(len(boxes))
        print "    current Box = {}".format(currBox.getStr())
    iteration+=1

    # split into 8 volumes
    root = currBox.corner
    w    = currBox.w
    h    = currBox.h
    d    = currBox.d

    newW       = w/2
    newW_round = (w+1)/2
    newH       = h/2
    newH_round = (h+1)/2
    newD       = d/2
    newD_round = (d+1)/2

    newW       = 1 if newW       == 0 else newW
    newW_round = 1 if newW_round == 0 else newW_round
    newH       = 1 if newH       == 0 else newH
    newH_round = 1 if newH_round == 0 else newH_round
    newD       = 1 if newD       == 0 else newD
    newD_round = 1 if newD_round == 0 else newD_round

    subVol0Loc = Location(root.x,        root.y,        root.z)
    subVol1Loc = Location(root.x + newW, root.y,        root.z)
    subVol2Loc = Location(root.x,        root.y + newH, root.z)
    subVol3Loc = Location(root.x + newW, root.y + newH, root.z)
    subVol4Loc = Location(root.x,        root.y,        root.z + newD)
    subVol5Loc = Location(root.x + newW, root.y,        root.z + newD)
    subVol6Loc = Location(root.x,        root.y + newH, root.z + newD)
    subVol7Loc = Location(root.x + newW, root.y + newH, root.z + newD)

    # +1s below are to round up if the w/h/d are odd
    subVol0 = Box(subVol0Loc, newW,       newH,       newD)
    subVol1 = Box(subVol1Loc, newW_round, newH,       newD)
    subVol2 = Box(subVol2Loc, newW,       newH_round, newD)
    subVol3 = Box(subVol3Loc, newW_round, newH_round, newD)
    subVol4 = Box(subVol4Loc, newW,       newH,       newD_round)
    subVol5 = Box(subVol5Loc, newW_round, newH,       newD_round)
    subVol6 = Box(subVol6Loc, newW,       newH_round, newD_round)
    subVol7 = Box(subVol7Loc, newW_round, newH_round, newD_round)

    # ADD LOGIC to not split if w/h/d is already 1
    subVols = []
    subVols.append(subVol0)
    if w != 1                      : subVols.append(subVol1)
    if            h != 1           : subVols.append(subVol2)
    if w != 1 and h != 1           : subVols.append(subVol3)
    if                       d != 1: subVols.append(subVol4)
    if w != 1 and            d != 1: subVols.append(subVol5)
    if            h != 1 and d != 1: subVols.append(subVol6)
    if w != 1 and h != 1 and d != 1: subVols.append(subVol7)

    # add bots
    for v in subVols:
        for b in currBox.bots:
            v.addPotentialBot(b)
        if len(v.bots) > 0:
            boxes.append(v)

    #print "----------------"
    #for idx, v in enumerate(subVols):
    #    print v.getStr()
print "======================"
maxBots = 0
optimalBox = None
for idx,b in enumerate(boxes):
    print b.getStr()
    if b.vol > 1: continue
    if len(b.bots) > maxBots:
        optimalBox = b
        maxBots = len(b.bots)

print "----------------"
print "optimal location:"
print optimalBox.getStr()


