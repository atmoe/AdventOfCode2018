#!/usr/bin/python

import sys
import re
import datetime
import string

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

steps = {}
for line in inputFile.readlines():
    regexStr = "^Step (\S) must be finished before step (\S) can begin.$"
    m = re.match(regexStr, line)
    assert m, "line doesnt match expectations! line = " + line
 
    step = m.group(2)
    dep  = m.group(1)

    if not step in steps: steps[step] = []
    if not dep  in steps: steps[dep]  = []

    steps[step].append(dep)

inputFile.close()

for s in steps:
    print s, " <- ", str(steps[s])

stepOrder = []
remainingSteps = dict(steps)

while len(remainingSteps) != 0:
    print "--------------------"

    # Find Ready Steps
    allReadySteps = []
    for s in remainingSteps:
        if len(remainingSteps[s]) == 0: allReadySteps.append(s)

    allReadySteps.sort()
    nextStep = allReadySteps[0]

    stepOrder.append(nextStep)

    # Remove
    print "ready steps = " + str(allReadySteps)
    del remainingSteps[nextStep]

    # Execute Steps
    for s in remainingSteps:
        i=0
        for d in remainingSteps[s]:
            if d == nextStep: del remainingSteps[s][i]
            i+=1


    for s in remainingSteps:
        print s, " <- ", str(remainingSteps[s])


print "".join(stepOrder)


second = 0
remainingSteps = dict(steps)

while len(remainingSteps) != 0:
    print "--------------------"

    # Update worker status
    # Remove complete steps

    # Find Ready Steps

    # Start new steps based on free workers

    # increment second
    second += 1





