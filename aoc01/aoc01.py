#!/usr/bin/python

import sys;

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")


adjustments = []
for line in inputFile.readlines():
    adjustments.append(int(line))

freq = 0
for val in adjustments:
    freq += val

print "Initial Frequencty = " + str(freq)

freq = 0
pastFrequencies = {}
foundSecondFrequency = False
while foundSecondFrequency == False:
    for val in adjustments:
        freq += val

        if(freq not in pastFrequencies):
            pastFrequencies[freq] = 1
        else:
            foundSecondFrequency = True
            break

print "Second Frequency = " + str(freq)


inputFile.close()