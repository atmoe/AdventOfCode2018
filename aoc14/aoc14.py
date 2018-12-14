#!/usr/bin/python

import sys
import re
import datetime
import string
import copy

def printRecipes(recipes):
    recipeStr = ""
    for idx, r in enumerate(recipes):
        if   idx == elfLoc1: recipeStr += "("+str(r)+")"
        elif idx == elfLoc2: recipeStr += "["+str(r)+"]"
        else:                recipeStr += " "+str(r)+" "
    print recipeStr


assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

numRecipes    = int(sys.argv[1])
numRecipesStr = str(sys.argv[1])
numRecipesLen = len(sys.argv[1])

elfLoc1 = 0
elfLoc2 = 1

recipes = [3, 7]
#printRecipes(recipes)

while len(recipes) < numRecipes + 10:
    recipeSum = recipes[elfLoc1] + recipes[elfLoc2]

    if(recipeSum >= 10):
        recipes.append(recipeSum/10)

    recipes.append(recipeSum % 10)

    elfLoc1 = (elfLoc1 + recipes[elfLoc1] + 1) % len(recipes)
    elfLoc2 = (elfLoc2 + recipes[elfLoc2] + 1) % len(recipes)

    #printRecipes(recipes)

print "Part 1: " + "".join(str(x) for x in recipes[numRecipes:numRecipes+10])

# Part 2
elfLoc1 = 0
elfLoc2 = 1

recipes = [3, 7]
valueFound = False
while not valueFound:
    recipeSum = recipes[elfLoc1] + recipes[elfLoc2]

    if(recipeSum >= 10):
        recipes.append(recipeSum/10)

    recipes.append(recipeSum % 10)

    elfLoc1 = (elfLoc1 + recipes[elfLoc1] + 1) % len(recipes)
    elfLoc2 = (elfLoc2 + recipes[elfLoc2] + 1) % len(recipes)

    # Check for match
    lastDigits1 = "".join(str(x) for x in recipes[-(numRecipesLen+1):-1])
    lastDigits2 = "".join(str(x) for x in recipes[-numRecipesLen:])

    if(lastDigits1 == numRecipesStr):
        valueFound = True
        print "Part 2: " + str(len(recipes)-(numRecipesLen+1))
    elif(lastDigits2 == numRecipesStr):
        valueFound = True
        print "Part 2: " + str(len(recipes)-numRecipesLen)

    #print "----------------------"
    #printRecipes(recipes)
    #print lastDigits1
    #print lastDigits2





