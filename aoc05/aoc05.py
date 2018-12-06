#!/usr/bin/python

import sys
import re
import datetime
import string

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")
lines = inputFile.readlines()
inputFile.close()
assert len(lines) == 1, "File not one line!"

originalPolymer = list(lines[0].strip())


minLength = len(originalPolymer)

for letter in list(string.ascii_lowercase):
    print letter

    reactionFound = True

    polymer = list(originalPolymer)
    i = 0
    while i < len(polymer)-1:
        if(polymer[i].lower() == letter):
            del polymer[i]
        else: 
            i+=1

    while reactionFound:
        reactionFound = False
        i = 0
        while i < len(polymer)-1:
            thisChar = polymer[i]
            nextChar = polymer[i+1]

            if(thisChar.isupper() != nextChar.isupper() and thisChar.upper() == nextChar.upper()):
                reactionFound = True
                del polymer[i+1]
                del polymer[i]
            else:
                i += 1


    if(minLength > len(polymer)): minLength = len(polymer)

print "Min Length = " + str(minLength)









