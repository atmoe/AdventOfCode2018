#!/usr/bin/python

import sys;

def boxIDCompare(boxID1, boxID2):
	if len(boxID1) != len(boxID2): return -1

	diffChars = 0
	for i in range(len(boxID1)):
		if boxID1[i] != boxID2[i]: diffChars+=1

	return diffChars

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

boxIDs = []
for line in inputFile.readlines():
	boxIDs.append(line.strip())

twoLetterIDs = 0
threeLetterIDs = 0
for boxID in boxIDs:
	letterDict = {}
	for letter in list(boxID):
		if(letter not in letterDict):
			letterDict[letter] = 1
		else:
			letterDict[letter] += 1    

	incrementTwo = False
	incrementThree = False
	for letter in letterDict:
		if letterDict[letter] == 2:	incrementTwo  = True
		if letterDict[letter] == 3:	incrementThree = True

	if incrementTwo:   twoLetterIDs+=1
	if incrementThree: threeLetterIDs+=1

print "Checksum = " + str(twoLetterIDs * threeLetterIDs)

for i in range(len(boxIDs)):
	for j in range(i+1, len(boxIDs)):
		if(boxIDCompare(boxIDs[i], boxIDs[j]) == 1):
			print boxIDs[i] + " " + boxIDs[j] + " => ",
			newID = ""
			for letter in range(len(boxIDs[i])):
				if boxIDs[i][letter] == boxIDs[j][letter]: newID += boxIDs[i][letter]
			print newID


inputFile.close()