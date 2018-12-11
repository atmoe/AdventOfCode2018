#!/usr/bin/python

import sys
import re
import datetime
import string
import copy

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")
lines = inputFile.readlines()
inputFile.close()
assert len(lines) == 1, "File not one line!"

serialNumber = int(lines[0])

grid = [[0 for x in range(300)] for y in range(300)]

for y in range(300):
    for x in range(300):
        rackID = (x+1) + 10
        powerLevel = rackID * (y+1)
        powerLevel += serialNumber
        powerLevel *= rackID
        powerLevel /= 100
        powerLevel %= 10
        powerLevel -= 5

        grid[y][x] = powerLevel

# Part 1
max3x3Val = 0
max3x3X   = 0
max3x3Y   = 0
for y in range(300-2):
    for x in range(300-2):
        val3x3  = 0
        for i in range(y,y+3):
            for j in range(x,x+3):
                val3x3+=grid[i][j]
        if(val3x3 > max3x3Val):
            max3x3Val = val3x3
            max3x3Y = y+1
            max3x3X = x+1

print "Max Part1 is ", max3x3Val, " at (", max3x3X, ", ", max3x3Y, ")"


# Part 2
gridSAT = [[0 for x in range(300)] for y in range(300)]
for y in range(300):
    for x in range(300):
        if x==0:
            val1 =0
        else: 
            val1 = gridSAT[y][x-1]

        if y==0:
            val2 =0
        else: 
            val2 = gridSAT[y-1][x]

        if y==0 or x==0:
            val3 =0
        else: 
            val3 = gridSAT[y-1][x-1]

        gridSAT[y][x] = grid[y][x] + val1 + val2 - val3

maxVal = 0
maxX   = 0
maxY   = 0
maxSz  = 0
for s in range(1, 301):
    for y in range(300-s):
        for x in range(300-s):
            if x==0 and y==0:
                A = 0
            else:
                A = gridSAT[y-1][x-1]

            if y==0:
                B = 0
            else:
                B = gridSAT[y-1][x+s-1]

            if x==0:
                C = 0
            else:
                C = gridSAT[y+s-1][x-1]

            D = gridSAT[y+s-1][x+s-1]

            val = D - B - C + A

            if(val > maxVal):
                maxVal = val
                maxY   = y+1
                maxX   = x+1
                maxSz  = s

print "Max Part2 is ", maxVal, " at (", maxX, ", ", maxY, ") with size = ", maxSz


