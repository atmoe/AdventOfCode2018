#!/usr/bin/python

import sys
import re
import datetime
import string
import copy

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

inputFile = open(sys.argv[1], "r")
lines = inputFile.readlines()
inputFile.close()
assert len(lines) == 1, "File not one line!"

m = re.match("^(\d+) players; last marble is worth (\d+) points$", lines[0])
assert m, "unexpected input! line = " + lines[0]

numPlayers = int(m.group(1))
numMarbles = int(m.group(2))*100 + 1
print "Players = ", numPlayers, " Marbles = ", numMarbles

scores = [0 for x in range(numPlayers)]
marbles = [0, 2, 1]
currentMarble = 1
currentElf = 2
for marble in range(3, numMarbles):
    if marble % 23 == 0:
        currentMarble = (currentMarble - 7) % len(marbles)
        scores[currentElf] += marble
        scores[currentElf] += marbles[currentMarble]
        del marbles[currentMarble]

    else:
        currentMarble = (currentMarble + 2) % len(marbles)
        marbles.insert(currentMarble, marble)

    #print currentElf, " -> ", marbles

    currentElf = (currentElf + 1) % numPlayers    


print "max score = ", max(scores)










