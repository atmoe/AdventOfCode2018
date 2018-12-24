#!/usr/bin/python

import sys
import re
import datetime
import string
import copy
import random

class Group:
    def __init__(self, gType, num, numUnits, hp, immuneTo, weakTo, ap, dType, initiative):
        self.gType      = gType
        self.num        = num
        self.numUnits   = numUnits
        self.hp         = hp
        self.weakTo     = weakTo
        self.immuneTo   = immuneTo
        self.ap         = ap
        self.dType      = dType
        self.initiative = initiative

    def isDead(self):
        return self.numUnits <= 0

    def takeDamage(self, damage):
        self.numUnits -= (damage / self.hp)

    def effectivePower(self):
        return self.numUnits * self.ap

    def getDamageTo(self, grp):
        if self.dType in grp.immuneTo: return 0

        if self.dType in grp.weakTo: return 2*self.effectivePower()

        return self.effectivePower()

    def getStr(self):
        grpStr =  "{} Group {}:\n".format(self.gType, self.num)
        grpStr += "  - Units  {}\n".format(self.numUnits)
        grpStr += "  - HP     {}\n".format(self.hp)
        grpStr += "  - AP     {}\n".format(self.ap)
        grpStr += "  - Damage {}\n".format(self.dType)
        grpStr += "  - Init   {}\n".format(self.initiative)
        grpStr += "  - Weak   {}\n".format(" / ".join(self.weakTo))
        grpStr += "  - Immune {}\n".format(" / ".join(self.immuneTo))

        return grpStr

def setTargets(attackers, defenders):
    targets = {}
    for a in attackers:
        if a.isDead(): continue

        target    = None
        for d in defenders:
            if d.isDead(): continue
            if d in targets.values() : continue

            if target==None:
                target = d
            else:
                if a.getDamageTo(target) < a.getDamageTo(d):
                    target = d
                elif a.getDamageTo(target) == a.getDamageTo(d):
                    if target.effectivePower() < d.effectivePower():
                        target = d
                    elif target.effectivePower() == d.effectivePower():
                        if target.initiative < d.initiative:
                            target = d

        targets[a]=target

    return targets

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 arguments!"

immuneGroups = []
infectionGroups = []
inputFile = open(sys.argv[1], "r")
gettingImmune    = False
gettingInfection = False
immuneGrpNum = 1
infectGrpNum = 1
for line in inputFile.readlines():
    immune    = re.match("^Immune System:", line)
    infection = re.match("^Infection:", line)
    group     = re.match("(\d+) units each with (\d+) hit points (\(.*\) )with an attack that does (\d+) (\S+) damage at initiative (\d+)", line)

    if immune:
        gettingImmune = True
        gettingInfection = False

    if infection:
        gettingImmune = False
        gettingInfection = True

    if group:
        print "here!"
        numUnits   = int(group.group(1))
        hp         = int(group.group(2))
        ap         = int(group.group(4))
        dType      = group.group(5)
        initiative = int(group.group(6))

        w      = re.search("weak to ((\w+(, |;|\)))+)", group.group(3))
        weakTo = w.group(1).replace(";","").replace(")","").split(", ") if w else []

        i        = re.search("immune to ((\w+(, |;|\)))+)", group.group(3))
        immuneTo = i.group(1).replace(";","").replace(")","").split(", ") if i else []
        if gettingImmune:
            immuneGroups.append(Group("Immune", immuneGrpNum, numUnits, hp, immuneTo, weakTo, ap, dType, initiative))
            immuneGrpNum+=1
        if gettingInfection:
            infectionGroups.append(Group("Infect", infectGrpNum, numUnits, hp, immuneTo, weakTo, ap, dType, initiative))
            infectGrpNum += 1 

inputFile.close()

print "Immune System:"
for g in immuneGroups:
    print g.getStr()

print
print "Infection:"
for g in infectionGroups:
    print g.getStr()
infectHasGrps = True
immuneHasGrps = True
turn = 0
while infectHasGrps and immuneHasGrps:
    print "==========================================="
    print "=== Turn {}".format(turn)
    print "==========================================="

    # Target Phase

    # put groups in targeting order
    immuneGroups.sort(key=lambda c: (c.effectivePower(), c.initiative), reverse=True)
    infectionGroups.sort(key=lambda c: (c.effectivePower(), c.initiative), reverse=True)

    # hashes of targets
    immuneTargets = {}
    infectTargets = {}
    immuneTargets = setTargets(immuneGroups, infectionGroups)
    infectTargets = setTargets(infectionGroups, immuneGroups)

    # Attach Phase
    allGroups = immuneGroups + infectionGroups
    allGroups.sort(key=lambda c: c.initiative, reverse=True)

    for attacker in allGroups:
        if attacker.isDead(): continue

        if   attacker.gType=="Immune" and attacker in immuneTargets.keys(): target = immuneTargets[attacker]
        elif attacker.gType=="Infect" and attacker in infectTargets.keys(): target = infectTargets[attacker]
        else: continue

        damage = attacker.getDamageTo(target)
        target.takeDamage(damage)

        print "{} {} attacks {} {} for {} damage".format(attacker.gType, attacker.num, target.gType, target.num, damage)

    print "Immune System:"
    immuneHasGrps = False
    for g in immuneGroups:
        if g.numUnits > 0:
            immuneHasGrps = True
            print g.getStr()

    print
    print "Infection:"
    infectHasGrps = False
    for g in infectionGroups:
        if g.numUnits > 0:
            infectHasGrps = True
            print g.getStr()


totalUnits = 0
allGroups = immuneGroups+infectionGroups
for g in allGroups:
    if g.numUnits > 0: totalUnits+=g.numUnits

print numUnits




