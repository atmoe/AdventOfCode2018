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

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

bots = []
inputFile = open(sys.argv[1], "r")
for line in inputFile.readlines():
    p = re.match("^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$", line)
    assert p, "invalid bot position.  line = {}".format(line)
    botLoc = Location(int(p.group(1)), int(p.group(2)), int(p.group(3)))
    bots.append(NanoBot(botLoc, int(p.group(4))))
inputFile.close()

bots.sort(key=lambda c: c.r, reverse=True)
strongestBot = bots[0]
weakestBot   = bots[-1]

botsInRange = 0
for b in bots:
    dist = b.loc.distTo(strongestBot.loc)

    if dist <= strongestBot.r:
        botsInRange += 1

print "Bots In Range of Strongest = {}".format(botsInRange)
print "Strongest Bot = {} r = {}".format(strongestBot.loc.getStr(), strongestBot.r)
print "Weakest Bot = {} r = {}".format(weakestBot.loc.getStr(), weakestBot.r)
print "Total Bots = {}".format(len(bots))

possiblePositions = []
for b1Idx in range(len(bots)):
    for b2Idx in range(b1Idx+1,len(bots)):
        b1 = bots[b1Idx]
        b2 = bots[b2Idx]
        distBetweenBots = b1.loc.distTo(b2.loc)

# For each bot, find all other bots that could share if it were just the two
