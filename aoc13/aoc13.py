#!/usr/bin/python

import sys
import re
import datetime
import string
import copy
import random

class Cart:
    def __init__(self, x, y, direction):
        self.x         = x
        self.y         = y
        self.direction = direction
        self.nextTurn  = "LEFT"

    def turnCorner(self, cornerType):
        if   self.direction == "^" and cornerType == "\\": self.direction = "<"
        elif self.direction == "^" and cornerType == "/":  self.direction = ">"
        elif self.direction == ">" and cornerType == "\\": self.direction = "v"
        elif self.direction == ">" and cornerType == "/":  self.direction = "^"
        elif self.direction == "v" and cornerType == "\\": self.direction = ">"
        elif self.direction == "v" and cornerType == "/":  self.direction = "<"
        elif self.direction == "<" and cornerType == "\\": self.direction = "^"
        elif self.direction == "<" and cornerType == "/":  self.direction = "v"
        else: assert 0, "did not turn!"


    def turnIntersection(self):
        if self.nextTurn == "LEFT":
            if   self.direction == "^": self.direction = "<"
            elif self.direction == ">": self.direction = "^"
            elif self.direction == "v": self.direction = ">"
            elif self.direction == "<": self.direction = "v"
            self.nextTurn = "STRAIGHT"

        elif self.nextTurn == "STRAIGHT":
            self.nextTurn = "RIGHT"

        elif self.nextTurn == "RIGHT":
            if   self.direction == "^": self.direction = ">"
            elif self.direction == ">": self.direction = "v"
            elif self.direction == "v": self.direction = "<"
            elif self.direction == "<": self.direction = "^"
            self.nextTurn = "LEFT"

    def move(self):
        if   self.direction == "^": self.y -= 1
        elif self.direction == "v": self.y += 1
        elif self.direction == "<": self.x -= 1
        elif self.direction == ">": self.x += 1

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

inputFile = open(sys.argv[1], "r")

grid  = []
carts = []
for y,line in enumerate(inputFile.readlines()):
    gridLine = []
    for x,c in enumerate(line):
        if c == "^" or c=="v":
            gridLine.append("|")
            carts.append(Cart(x, y, c))
        elif c == ">" or c=="<":
            gridLine.append("-")
            carts.append(Cart(x, y, c))
        elif c != '\n':
            gridLine.append(c)

    grid.append(gridLine)

inputFile.close()

for g in grid:
    print "".join(g)


carts.sort(key=lambda c: (c.y, c.x))
for cart in carts:
    print cart.x, " ", cart.y, " ", cart.direction

# Ticks
# - move carts
# - check for collisions

printGrid = False
avoidCollisions = False
tick = 0
collisionOccurred = False
while not collisionOccurred or (avoidCollisions and len(carts) > 1):
    tick += 1
    print "Tick: ", tick, " Carts left = ", len(carts)

    # sort carts
    carts.sort(key=lambda c: (c.y, c.x))

    # move carts
    cartsToRemove = []
    for cart in carts:
        cart.move()

        gridType = grid[cart.y][cart.x]

        assert gridType != " ", "cart (" + str(cart.x) + ", " + str(cart.y) + ") off track!"

        if   gridType == "+":
            cart.turnIntersection()
        elif gridType == "\\" or gridType == "/":
            cart.turnCorner(gridType)
        else:
            assert gridType == "|" or gridType=="-", "incorrect grid type! type = '" + gridType + "'"

        # check for collisions
        for i in range(len(carts)):
            for j in range(i+1, len(carts)):
                if j in cartsToRemove: continue
                if i in cartsToRemove: continue
                if (carts[i].x == carts[j].x) and (carts[i].y == carts[j].y):
                    collisionOccurred = True
                    collisionX = carts[i].x
                    collisionY = carts[i].y
                    print "Collision = (", collisionX, ", ", collisionY, ")"
                    cartsToRemove.append(i)
                    cartsToRemove.append(j)

    cartsToRemove.sort(reverse=True)
    for r in cartsToRemove:
        del carts[r]


    if printGrid:
        gridCopy = copy.deepcopy(grid)
        for cart in carts:
            gridCopy[cart.y][cart.x] = cart.direction

        print "------------------"
        for g in gridCopy:
            print "".join(g)
        #for cart in carts:
        #    print cart.x, " ", cart.y, " ", cart.direction

    #a = raw_input("continue?")
    #if a == "n": break


if(len(carts)==1):
    print "Last Cart at (", carts[0].x, ", ", carts[0].y, ")"

if(len(carts)==0):
    print "No carts left!"





