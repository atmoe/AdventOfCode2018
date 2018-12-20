#!/usr/bin/python

import sys
import re
import datetime
import string
import copy

assert len(sys.argv) == 3, sys.argv[0] + " requires 2 arguments!"

numGens = int(sys.argv[2])
inputFile = open(sys.argv[1], "r")

initialState = ""
rules = {}
rules["....."] = "."
rules["....#"] = "."
rules["...#."] = "."
rules["...##"] = "."
rules["..#.."] = "."
rules["..#.#"] = "."
rules["..##."] = "."
rules["..###"] = "."
rules[".#..."] = "."
rules[".#..#"] = "."
rules[".#.#."] = "."
rules[".#.##"] = "."
rules[".##.."] = "."
rules[".##.#"] = "."
rules[".###."] = "."
rules[".####"] = "."
rules["#...."] = "."
rules["#...#"] = "."
rules["#..#."] = "."
rules["#..##"] = "."
rules["#.#.."] = "."
rules["#.#.#"] = "."
rules["#.##."] = "."
rules["#.###"] = "."
rules["##..."] = "."
rules["##..#"] = "."
rules["##.#."] = "."
rules["##.##"] = "."
rules["###.."] = "."
rules["###.#"] = "."
rules["####."] = "."
rules["#####"] = "."

for line in inputFile.readlines():
    init = re.match("^initial state: (.*)$", line)
    rule = re.match("^([#\.]{5}) => ([#\.])$", line)

    if init: initialState = init.group(1)
    if rule: rules[rule.group(1)] = rule.group(2)

inputFile.close()

print "init = ", initialState
print "-------------------------------------------"
for idx,r in enumerate(rules):
    print idx, ": ", r, "=>", rules[r]

print "-------------------------------------------"

initialState = "....." + initialState + "....."

cumulativeFilledPots = 0
firstPotIndex = -5
prevGen = initialState
lastGen = 0

for g in range(1,min([numGens, 1000000])+1): # assumes the input eventually degenerates before this value
    newGen = ".."

    for p in range(2,len(prevGen) - 2):
        ruleIdx = prevGen[p-2:p+3]
        newGen += rules[ruleIdx]

    # grow in positive direction
    if   newGen[-1] != ".": newGen += "..."
    elif newGen[-2] != ".": newGen += ".."
    elif newGen[-3] != ".": newGen += "."
    newGen += ".."

    # Grow in negative direction
    if newGen[2] == "#":
        newGen = "..." + newGen
        firstPotIndex -= 3
    elif newGen[3] == "#":
        newGen = ".." + newGen
        firstPotIndex -= 2
    elif newGen[4] == "#":
        newGen = "." + newGen
        firstPotIndex -= 1

    # Trim pots
    firstPotWithPlant = 0
    for i in range(len(newGen)):
        if newGen[i]=="#":
            firstPotWithPlant = i
            break

    newGen = newGen[firstPotWithPlant-5:]
    firstPotIndex += (firstPotWithPlant-5)

    potSum = 0
    for i in range(len(newGen)):
        if newGen[i] == "#": potSum += i + firstPotIndex

    assert newGen[0:5] == ".....", "Not enough negative empty pots.  Gen = " + newGen + " gen = " + str(g)
    assert newGen[-5:] == ".....", "Not enough positive empty pots.  Gen = " + newGen
 
    lastGen = g
    if(prevGen == newGen): break

    prevGen = newGen
    prevPotSum = potSum

# adjust first index
print "last gen = ", lastGen, " remaining Generations = ", numGens - lastGen
firstPotIndex += numGens - lastGen


potSum = 0
for i in range(len(prevGen)):
    if prevGen[i] == "#": potSum += i + firstPotIndex

print "Pot Sum = ", potSum

