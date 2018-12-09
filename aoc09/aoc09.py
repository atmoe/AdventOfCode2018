#!/usr/bin/python

import sys
import re
import datetime
import string
import copy

class Node:
    def __init__(self, value, prev, nxt):
        self.value = value
        self.prev  = prev
        self.next  = nxt

    def updatePrev(self, newPrev):
        self.prev = newPrev

    def updateNext(self, newNxt):
        self.next = newNxt

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")
lines = inputFile.readlines()
inputFile.close()
assert len(lines) == 1, "File not one line!"

m = re.match("^(\d+) players; last marble is worth (\d+) points$", lines[0])
assert m, "unexpected input! line = " + lines[0]

isPart2 = True
if isPart2: multiplier = 100
else:       multiplier = 1

numPlayers = int(m.group(1))
numMarbles = int(m.group(2))*multiplier + 1
print "Players = ", numPlayers, " Marbles = ", numMarbles

scores = [0 for x in range(numPlayers)]

useArray = False
if useArray:
    marbles = [0, 2, 1]
    currentMarble = 1
    currentElf = 2
    for marble in range(3, numMarbles):
        #print marble, " ", marble/(float)numMarbles, "%"
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

else:
    # use linked list
    marble0 = Node(0, None, None)
    marble1 = Node(1, None, None)
    marble2 = Node(2, None, None)

    marble0.updatePrev(marble1)
    marble0.updateNext(marble2)
    marble1.updatePrev(marble2)
    marble1.updateNext(marble0)
    marble2.updatePrev(marble0)
    marble2.updateNext(marble1)

    currentMarble = marble2
    currentElf = 2

    for marble in range(3, numMarbles):
        #print marble, " ", 100*marble/float(numMarbles), "%"
        if marble % 23 == 0:
            scores[currentElf] += marble

            for i in range(7):
                currentMarble = currentMarble.prev


            scores[currentElf] += currentMarble.value

            currentMarble.prev.updateNext(currentMarble.next)
            currentMarble.next.updatePrev(currentMarble.prev)

            currentMarble = currentMarble.next

        else:
            newMarble = Node(marble, currentMarble.next, currentMarble.next.next)
            currentMarble.next.next.updatePrev(newMarble)
            currentMarble.next.updateNext(newMarble)
            currentMarble = newMarble
        '''
        printMarb = marble0.prev
        print "0 -> ",
        while printMarb != marble0:
            print printMarb.value, " -> ",
            printMarb = printMarb.prev
        print 
        '''
        currentElf = (currentElf + 1) % numPlayers    

print "max score = ", max(scores)










