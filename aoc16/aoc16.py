#!/usr/bin/python

import sys
import re
import datetime
import string
import copy
import random

class Sample:
    def __init__(self):
        self.regInput  = [0,0,0,0]
        self.microCode = [0,0,0,0]
        self.regResult = [0,0,0,0]


def execOp(op, A, B, C, regs):
    resultRegs = copy.deepcopy(regs)
    if   op == "addr": resultRegs[C] = regs[A] + regs[B]
    elif op == "addi": resultRegs[C] = regs[A] + B
    elif op == "mulr": resultRegs[C] = regs[A] * regs[B]
    elif op == "muli": resultRegs[C] = regs[A] * B
    elif op == "banr": resultRegs[C] = regs[A] & regs[B]
    elif op == "bani": resultRegs[C] = regs[A] & B
    elif op == "borr": resultRegs[C] = regs[A] | regs[B]
    elif op == "bori": resultRegs[C] = regs[A] | B
    elif op == "setr": resultRegs[C] = regs[A]
    elif op == "seti": resultRegs[C] = A
    elif op == "gtir": resultRegs[C] = 1 if A > regs[B] else 0
    elif op == "gtri": resultRegs[C] = 1 if regs[A] > B else 0
    elif op == "gtrr": resultRegs[C] = 1 if regs[A] > regs[B] else 0
    elif op == "eqir": resultRegs[C] = 1 if A == regs[B] else 0
    elif op == "eqri": resultRegs[C] = 1 if regs[A] == B else 0
    elif op == "eqrr": resultRegs[C] = 1 if regs[A] == regs[B] else 0
    else: assert 0, "unknown op! op = " + op

    return resultRegs

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

inputFile = open(sys.argv[1], "r")

beforeSeen = False
microSeen  = False

fullMicrocode = []
samples = []
for idx,line in enumerate(inputFile.readlines()):
    if not beforeSeen: 
        beforeLine = re.match("^Before: \[(\d+), (\d+), (\d+), (\d+)\]$", line)
        if beforeLine:
            regInput = [int(beforeLine.group(1)), int(beforeLine.group(2)), int(beforeLine.group(3)), int(beforeLine.group(4))]
            beforeSeen = True

        fullMicroLine = re.match("^(\d+) (\d+) (\d+) (\d+)$", line)
        if fullMicroLine:
            fullMicrocode.append([int(fullMicroLine.group(1)), int(fullMicroLine.group(2)), int(fullMicroLine.group(3)), int(fullMicroLine.group(4))])

    elif beforeSeen and not microSeen:
        microLine = re.match("^(\d+) (\d+) (\d+) (\d+)$", line)
        micro = [int(microLine.group(1)), int(microLine.group(2)), int(microLine.group(3)), int(microLine.group(4))]
        microSeen = True

    elif beforeSeen and microSeen:
        afterLine = re.match("^After:  \[(\d+), (\d+), (\d+), (\d+)\]$", line)
        regResult = [int(afterLine.group(1)), int(afterLine.group(2)), int(afterLine.group(3)), int(afterLine.group(4))]
        beforeSeen=False
        microSeen=False

        newSample = Sample()
        newSample.regInput  = regInput
        newSample.micro     = micro
        newSample.regResult = regResult

        samples.append(newSample)

inputFile.close()

knownOps     = ["" for x in range(16)]
knownOps[0]  = "addi"
knownOps[1]  = "eqrr"
knownOps[2]  = "borr"
knownOps[3]  = "gtri"
knownOps[4]  = "addr"
knownOps[5]  = "seti"
knownOps[6]  = "muli"
knownOps[7]  = "bani"
knownOps[8]  = "banr"
knownOps[9]  = "gtrr"
knownOps[10] = "setr"
knownOps[11] = "gtir"
knownOps[12] = "bori"
knownOps[13] = "eqri"
knownOps[14] = "eqir"
knownOps[15] = "mulr"

print knownOps

unknownOpcodes = [
#"addr",
#"addi",
#"mulr",
#"muli",
#"banr",
#"bani",
#"borr",
#"bori",
#"setr",
#"seti",
#"gtir",
#"gtri",
#"gtrr",
#"eqir",
#"eqri",
#"eqrr"
]
match1 = 0
match2 = 0
match3orMore = 0
for s in samples:
    numMatchingOps = 0
    matchingOps    = []

    for op in unknownOpcodes:
        result = execOp(op, s.micro[1], s.micro[2], s.micro[3], s.regInput)

        resultsMatch = result[0] == s.regResult[0] and result[1] == s.regResult[1] and result[2] == s.regResult[2] and result[3] == s.regResult[3]
        if(resultsMatch):
            numMatchingOps += 1
            matchingOps.append(op)

    if numMatchingOps >= 3: match3orMore+=1
    if numMatchingOps== 2: match2 +=1
    if numMatchingOps== 1: match1 +=1

    if numMatchingOps==1:
        print matchingOps[0], " = ", s.micro[0] 

print "match 1 = ", match1
print "match 2 = ", match2
print "match 3 or more = ", match3orMore


registers = [0,0,0,0]
for inst in fullMicrocode:
    print inst[0]
    print knownOps[inst[0]]
    registers = execOp(knownOps[inst[0]], inst[1], inst[2], inst[3], registers)

print registers[0]
