#!/usr/bin/python

import sys
import re
import datetime
import string
import copy
import random

class Instruction:
    def __init__(self, op, A, B, C):
        self.op = op
        self.A  = A
        self.B  = B
        self.C  = C
    def printInst(self):
        print "{} {} {} {}".format(self.op, self.A, self.B, self.C),

def execOp(inst, regs):
    resultRegs = copy.deepcopy(regs)
    if   inst.op == "addr": resultRegs[inst.C] = regs[inst.A] + regs[inst.B]
    elif inst.op == "addi": resultRegs[inst.C] = regs[inst.A] + inst.B
    elif inst.op == "mulr": resultRegs[inst.C] = regs[inst.A] * regs[inst.B]
    elif inst.op == "muli": resultRegs[inst.C] = regs[inst.A] * inst.B
    elif inst.op == "banr": resultRegs[inst.C] = regs[inst.A] & regs[inst.B]
    elif inst.op == "bani": resultRegs[inst.C] = regs[inst.A] & inst.B
    elif inst.op == "borr": resultRegs[inst.C] = regs[inst.A] | regs[inst.B]
    elif inst.op == "bori": resultRegs[inst.C] = regs[inst.A] | inst.B
    elif inst.op == "setr": resultRegs[inst.C] = regs[inst.A]
    elif inst.op == "seti": resultRegs[inst.C] = inst.A
    elif inst.op == "gtir": resultRegs[inst.C] = 1 if inst.A > regs[inst.B] else 0
    elif inst.op == "gtri": resultRegs[inst.C] = 1 if regs[inst.A] > inst.B else 0
    elif inst.op == "gtrr": resultRegs[inst.C] = 1 if regs[inst.A] > regs[inst.B] else 0
    elif inst.op == "eqir": resultRegs[inst.C] = 1 if inst.A == regs[inst.B] else 0
    elif inst.op == "eqri": resultRegs[inst.C] = 1 if regs[inst.A] == inst.B else 0
    elif inst.op == "eqrr": resultRegs[inst.C] = 1 if regs[inst.A] == regs[inst.B] else 0
    else: assert 0, "unknown op! op = " + inst.op

    return resultRegs

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

inputFile = open(sys.argv[1], "r")

instPtrReg = 0
microcode = []
for idx,line in enumerate(inputFile.readlines()):
    if idx == 0:
        ptr = re.match("^#ip (\d)", line)
        assert ptr, "invalid first line"
        instPtrReg = int(ptr.group(1))
    else:
        inst = re.match("^(....) (\d+) (\d+) (\d+)", line)
        assert inst, "unexpected instruction = " + line
        nextInst = Instruction(inst.group(1), int(inst.group(2)), int(inst.group(3)), int(inst.group(4)))
        microcode.append(nextInst)

inputFile.close()

ipVal = 0
registers = [0,0,0,0,0,0]
while ipVal < len(microcode):
    inst = microcode[ipVal]
    registers[instPtrReg] = ipVal

    print "ip={0:2} [".format(ipVal), 
    for r in registers:
        print "{0:5}".format(r),
    print "] ",
    inst.printInst()

    registers = execOp(inst, registers)

    print "[",
    for r in registers:
        print "{0:5}".format(r),
    print "] "

    ipVal = registers[instPtrReg]
    ipVal+=1

print "------------------------------------------------"
print "Final Registers = ", registers
print "------------------------------------------------"
