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

    def hashKey(self):
        return str(self.y) + "_" + str(self.x)

class Unit:
    def __init__(self, uType, x, y):
        self.uType = uType
        self.loc   = Location(x,y)
        self.hp    = 200
        if uType == "E":
            self.ap = 3  # Change this for part 2
        else:
            self.ap = 3 

    def printUnit(self):
        print self.uType + "(" + str(self.loc.x) + ", " + str(self.loc.y) + ")  HP: " + str(self.hp)

    def enemyInRange(self, enemies):
        for e in enemies:
            if self.loc.adjacentTo(e.loc):
                return True

    def move(self, grid, enemies, units):
        # Generate grid of distances from self
        # Treat other units as walls
        distGrid = copy.deepcopy(grid)
        for u in units:
            if not u.isDead():
                distGrid[u.loc.y][u.loc.x] = "#"

        dist = 0
        currLocs = {}
        currLocs[str(self.loc.x)+"_"+str(self.loc.y)] = self.loc
        while currLocs:
            nextLocs = {}
            for locKey in currLocs:
                thisLoc = currLocs[locKey]
                distGrid[thisLoc.y][thisLoc.x] = str(dist)

                upFree    = distGrid[thisLoc.y-1][thisLoc.x] == "."
                downFree  = distGrid[thisLoc.y+1][thisLoc.x] == "."
                leftFree  = distGrid[thisLoc.y][thisLoc.x-1] == "."
                rightFree = distGrid[thisLoc.y][thisLoc.x+1] == "."

                if upFree:    nextLocs[str(thisLoc.x)+"_"+str(thisLoc.y-1)] = Location(thisLoc.x, thisLoc.y-1)
                if downFree:  nextLocs[str(thisLoc.x)+"_"+str(thisLoc.y+1)] = Location(thisLoc.x, thisLoc.y+1)
                if leftFree:  nextLocs[str(thisLoc.x-1)+"_"+str(thisLoc.y)] = Location(thisLoc.x-1, thisLoc.y)
                if rightFree: nextLocs[str(thisLoc.x+1)+"_"+str(thisLoc.y)] = Location(thisLoc.x+1, thisLoc.y)

            dist+=1
            currLocs.clear()
            for key in nextLocs:
                currLocs[key] = nextLocs[key]
            nextLocs.clear()

        #print "======================"
        #for l in distGrid:
        #    print "".join(l)

        # get closest in range location neighboring enemy
        closestLoc  = Location(0,0)
        closestDist = 1000000
        for e in enemies:
            up    = Location(e.loc.x, e.loc.y-1)
            down  = Location(e.loc.x, e.loc.y+1)
            left  = Location(e.loc.x-1, e.loc.y)
            right = Location(e.loc.x+1, e.loc.y)

            for i in [up, down, left, right]:
                if distGrid[i.y][i.x] != "." and distGrid[i.y][i.x] != "#":
                    distance = int(distGrid[i.y][i.x])
                    if distance < closestDist:
                        closestDist = distance
                        closestLoc  = i
                    elif distance == closestDist and i.earlierReadingOrderThan(closestLoc):
                        closestDist = distance
                        closestLoc  = i

        # no enemy in range
        if(closestDist == 1000000):
            return

        distGrid[closestLoc.y][closestLoc.x] = "+"

        # Choose direction to move
        distGridCloseLoc = copy.deepcopy(grid)
        for u in units:
            if not u.isDead():
                distGridCloseLoc[u.loc.y][u.loc.x] = "#"

        dist = 0
        currLocs = {}
        currLocs[str(closestLoc.x)+"_"+str(closestLoc.y)] = closestLoc
        while currLocs:
            nextLocs = {}
            for locKey in currLocs:
                thisLoc = currLocs[locKey]
                distGridCloseLoc[thisLoc.y][thisLoc.x] = str(dist)

                upFree    = distGridCloseLoc[thisLoc.y-1][thisLoc.x] == "."
                downFree  = distGridCloseLoc[thisLoc.y+1][thisLoc.x] == "."
                leftFree  = distGridCloseLoc[thisLoc.y][thisLoc.x-1] == "."
                rightFree = distGridCloseLoc[thisLoc.y][thisLoc.x+1] == "."

                if upFree:    nextLocs[str(thisLoc.x)+"_"+str(thisLoc.y-1)] = Location(thisLoc.x, thisLoc.y-1)
                if downFree:  nextLocs[str(thisLoc.x)+"_"+str(thisLoc.y+1)] = Location(thisLoc.x, thisLoc.y+1)
                if leftFree:  nextLocs[str(thisLoc.x-1)+"_"+str(thisLoc.y)] = Location(thisLoc.x-1, thisLoc.y)
                if rightFree: nextLocs[str(thisLoc.x+1)+"_"+str(thisLoc.y)] = Location(thisLoc.x+1, thisLoc.y)

            dist+=1
            currLocs.clear()
            for key in nextLocs:
                currLocs[key] = nextLocs[key]
            nextLocs.clear()

        up    = Location(self.loc.x, self.loc.y-1)
        down  = Location(self.loc.x, self.loc.y+1)
        left  = Location(self.loc.x-1, self.loc.y)
        right = Location(self.loc.x+1, self.loc.y)

        moveLoc     = Location(0,0)
        moveLocDist = 1000000
        for i in [up, down, left, right]:
            if distGridCloseLoc[i.y][i.x] != "." and distGridCloseLoc[i.y][i.x] != "#":
                distance = int(distGridCloseLoc[i.y][i.x])
                if distance < moveLocDist:
                    moveLocDist = distance
                    moveLoc     = i
                elif distance == moveLocDist and i.earlierReadingOrderThan(moveLoc):
                    moveLocDist = distance
                    moveLoc     = i
        '''
        distGrid[moveLoc.y][moveLoc.x] = "x"

        print "======================"
        for l in distGrid:
            print "".join(l)
        '''

        self.loc = moveLoc

    def attack(self, enemies):
        enemyToAttack=None
        for e in enemies:
            if self.loc.adjacentTo(e.loc):
                if enemyToAttack == None:
                    enemyToAttack = e
                elif enemyToAttack.hp > e.hp:
                    enemyToAttack = e
                elif enemyToAttack.hp == e.hp and e.loc.earlierReadingOrderThan(enemyToAttack.loc):
                    enemyToAttack = e

        assert enemyToAttack, "did not find enemy to attack!"

        enemyToAttack.takeDamage(self.ap)
        if enemyToAttack.isDead(): 
            enemies.remove(enemyToAttack)

    def takeDamage(self, damage):
        self.hp -= damage

    def isDead(self):
        return self.hp <=0


assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

inputFile = open(sys.argv[1], "r")

grid    = []
elves   = []
goblins = []
for y,line in enumerate(inputFile.readlines()):
    gridLine = []
    for x,c in enumerate(line):
        if c == "G":
            gridLine.append(".")
            goblins.append(Unit("G", x, y))
        elif c == "E":
            gridLine.append(".")
            elves.append(Unit("E", x, y))
        elif c != '\n':
            gridLine.append(c)

    grid.append(gridLine)

inputFile.close()

numElves = len(elves)

gameOver = False

for l in grid:
    print "".join(l)

for g in goblins:
    g.printUnit()
for e in elves:
    e.printUnit()

currRound = 1
while not gameOver:
#for i in range(3):
    # sort units by reading order
    units = goblins + elves
    units.sort(key=lambda c: (c.loc.y, c.loc.x))

    for unit in units:
        if unit.isDead(): continue

        # Check if there are targets left
        if unit.uType == "G": enemies = elves
        if unit.uType == "E": enemies = goblins

        gameOver = (len(enemies) == 0)
        if gameOver: break

        # Move if not adjacent to enemy
        if not unit.enemyInRange(enemies):
            unit.move(grid, enemies, units)

        if unit.enemyInRange(enemies):
            unit.attack(enemies)

    print "-----------------------------"
    print "--- Round ", currRound
    print "-----------------------------"
    printGrid = copy.deepcopy(grid)
    for u in units:
        if not u.isDead():
            printGrid[u.loc.y][u.loc.x] = u.uType
    for l in printGrid:
        print "".join(l)
    for g in goblins:
        g.printUnit()
    for e in elves:
        e.printUnit()

    currRound += 1

remainingHP = 0
for i in units:
    if not i.isDead():
        remainingHP += i.hp

print "game over!"
print "currRound = ", currRound
print "hp        = ", remainingHP
print "elves died", numElves - len(elves)
print "outcome = ", (currRound-2)*remainingHP
