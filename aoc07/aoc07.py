#!/usr/bin/python

import sys
import re
import datetime
import string
import copy

def getSeconds(letter):
    const = 60
    return const + ord(letter) - ord("A") + 1

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


# Part 1
stepOrder = []
remainingSteps = copy.deepcopy(steps)

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
        for idx, d in enumerate(remainingSteps[s]):
            if d == nextStep: del remainingSteps[s][idx]


    for s in remainingSteps:
        print s, " <- ", str(remainingSteps[s])


print "".join(stepOrder)


# Part 2
second = 0
remainingSteps = copy.deepcopy(steps)
inProgressSteps = []
completeSteps = []
workers = [0, 0, 0, 0, 0]  # value indicates seconds of work remaining
workerStep = ["","","","",""]
while len(remainingSteps) != 0:
#for isdf in range(4):
    print "-------------------"
    print "START Second    = ", second

    # Update Workers
    for idx_w, w in enumerate(workers):
        if w != 0:
            workers[idx_w] -= 1

            # Worker Finished
            if workers[idx_w] == 0:
                completedStep = workerStep[idx_w]
                completeSteps.append(completedStep)

                # remove in progress steps
                for idx_p, s in enumerate(inProgressSteps):
                    if s == completedStep: del inProgressSteps[idx_p]

                # Free Dependency from remaining steps
                for s in remainingSteps:
                    for idx_r, r in enumerate(remainingSteps[s]):
                        if r == completedStep: del remainingSteps[s][idx_r]

                # Remove step as remaining
                del remainingSteps[completedStep]

    # Find Ready Steps
    readySteps = []
    for s in remainingSteps:
        if (len(remainingSteps[s]) == 0) and not s in inProgressSteps: readySteps.append(s)

    readySteps.sort()

    print "Ready Steps       = ", readySteps

    # Start new steps based on free workers
    if len(readySteps) > 0:
        for idx_w, w in enumerate(workers):
            if w == 0:
                step = readySteps.pop()
                workers[idx_w] = getSeconds(step)
                workerStep[idx_w] = step
                inProgressSteps.append(step)
                if len(readySteps) == 0: break

    print "In Progress Steps = ", inProgressSteps
    print "Workers         = ", workers
    print "Workers Steps   = ", workerStep
    print "Remaining Steps = ", remainingSteps

    # increment second
    second += 1

