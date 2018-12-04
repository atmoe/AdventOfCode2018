#!/usr/bin/python

import sys;
import re;

class Claim:
    num  = -1
    xLoc = -1
    yLoc = -1
    w    = -1
    h    = -1

    def getStr(self):
        return str(self.num) + ": " + str(self.xLoc) + "," + str(self.yLoc) + " " + str(self.w) + "x" + str(self.h)


assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

claims = []
maxX = -1
maxY = -1

# --- Collect Claims ---
regexStr = "^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$"
for line in inputFile.readlines():
    m = re.match(regexStr, line)
    assert m, "Line did not match regex! line = \"" + line + "\""

    claim = Claim()
    claim.num  = int(m.group(1))
    claim.xLoc = int(m.group(2))
    claim.yLoc = int(m.group(3))
    claim.w    = int(m.group(4))
    claim.h    = int(m.group(5))

    claims.append(claim)

    if maxX < (claim.xLoc + claim.w - 1): maxX = claim.xLoc + claim.w - 1
    if maxY < (claim.yLoc + claim.h - 1): maxY = claim.yLoc + claim.h - 1

inputFile.close()

print "Total Size = " + str(maxX+1) + "x" + str(maxY+1)

rect = [[0 for x in range(maxX+1)] for y in range(maxY+1)]

for claim in claims:
    for y in range(claim.yLoc, claim.yLoc + claim.h):
        for x in range(claim.xLoc, claim.xLoc + claim.w):
            rect[y][x] += 1

overlaps = 0
for y in range(maxY+1):
    for x in range(maxX+1):
        if rect[y][x] > 1: overlaps+=1

print "Number of Inches with Overlap = " + str(overlaps)

for claim in claims:
    claimOverlaps = False
    for y in range(claim.yLoc, claim.yLoc + claim.h):
        for x in range(claim.xLoc, claim.xLoc + claim.w):
            if rect[y][x] > 1: claimOverlaps = True

    if not claimOverlaps: print "Claim with overlaps: " + str(claim.num)

