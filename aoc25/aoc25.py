#!/usr/bin/python

import sys
import re
import datetime
import string
import copy
import random


class Star:
    def __init__(self, x, y, z, t):
        self.x = x
        self.y = y
        self.z = z
        self.t = t

    def getStr(self):
        return "({}, {}, {}, {})".format(self.x, self.y, self.z, self.t)

    def distTo(self, star):
        return abs(self.x - star.x) + abs(self.y - star.y) + abs(self.z - star.z) + abs(self.t - star.t)

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

stars = []

inputFile = open(sys.argv[1], "r")
for line in inputFile.readlines():
    p = re.match("^(-?\d+),(-?\d+),(-?\d+),(-?\d+)$", line)
    assert p, "invalid star position.  line = {}".format(line)
    star = Star(int(p.group(1)), int(p.group(2)), int(p.group(3)), int(p.group(4)))
    stars.append(Star(int(p.group(1)), int(p.group(2)), int(p.group(3)), int(p.group(4))))

inputFile.close()

constellations = [] 
for sIdx, s in enumerate(stars):
    if sIdx%100 == 0: print "processing start {} of {}".format(sIdx, len(stars))

    memberOfConsts = []
    for idx,c in enumerate(constellations):
        for star in c:
            if(s.distTo(star) <= 3):
                memberOfConsts.append(idx)
                break

    if len(memberOfConsts) == 0:
        # new constellation
        constellations.append([s])
    elif len(memberOfConsts) == 1:
        # only part of one constellation, add to it
        constellations[memberOfConsts[0]].append(s)
    elif len(memberOfConsts) > 1:
        # part of multiple constellations, merge them
        for i in range(1, len(memberOfConsts)):
            constellations[memberOfConsts[0]] += constellations[memberOfConsts[i]]
            
        constellations[memberOfConsts[0]].append(s)
        
        # delete merged entries
        #    - reverse list to not change indices
        for i in reversed(range(1, len(memberOfConsts))):
            del constellations[memberOfConsts[i]]

totalStars = 0
for idx,c in enumerate(constellations):
    print "--------------------------------"
    print "--- constellation {}".format(idx)
    print "--------------------------------"
    for s in c:
        print s.getStr()
        totalStars+=1

print "================"
print "total stars          = {}".format(totalStars)
print "total constellations = {}".format(len(constellations))
print "================"
