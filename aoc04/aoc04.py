#!/usr/bin/python

import sys
import re
import datetime

class EnumEventType:
    Begin, Asleep, Wakeup = range(3)

class Event:
    def __init__(self):
        self.date  = datetime.datetime(1000,1,1,0,0,0)
        self.eType = -1  # enum above
        self.guardNum = -1  # only valid for a begin event

    def getStr(self):
        return str(self.num) + ": " + str(self.xLoc) + "," + str(self.yLoc) + " " + str(self.w) + "x" + str(self.h)

class Guard:
    def __init__(self):
        self.totalMinutesSlept = 0
        self.minutesHistogram = [0 for x in range(60)]

assert len(sys.argv) == 2, sys.argv[0] + " requires 1 argument!"

inputFile = open(sys.argv[1], "r")

events = []

# --- Collect Events ---
dateRegEx   = "\[(\d+)\-(\d+)\-(\d+) (\d+):(\d+)\]"
beginsRegEx = "\[.*\] Guard #(\d+) begins shift"
asleepRegEx = "\[.*\] falls asleep"
wakeupRegEx = "\[.*\] wakes up"
for line in inputFile.readlines():
    matchDate = re.match(dateRegEx, line)
    assert matchDate, "Line did not have a date! line = \"" + line + "\""

    matchBegin  = re.match(beginsRegEx, line)
    matchAsleep = re.match(asleepRegEx, line)
    matchWakeup = re.match(wakeupRegEx, line)
    assert matchBegin or matchWakeup or matchAsleep, "Line did not match event! line = \"" + line + "\""

    event = Event()

    event.date = datetime.datetime(
        int(matchDate.group(1)), 
        int(matchDate.group(2)),
        int(matchDate.group(3)),
        int(matchDate.group(4)), 
        int(matchDate.group(5)), 0)

    if(matchBegin):
        event.eType    = EnumEventType.Begin
        event.guardNum = matchBegin.group(1)
    elif(matchAsleep):
        event.eType = EnumEventType.Asleep
    elif(matchWakeup):
        event.eType = EnumEventType.Wakeup


    events.append(event)


inputFile.close()

events.sort(key=lambda x:x.date, reverse=False)

guards = {}
currentGuard = -1
currentGuardState = -1
currentAsleepMinute = -1
for evt in events: 
    assert (currentGuard != -1) or evt.eType==EnumEventType.Begin, "first event is not a guard taking a shift!"

    if(evt.eType == EnumEventType.Begin):
        currentGuardState = EnumEventType.Begin
        currentGuard = evt.guardNum

        if(currentGuard not in guards):
            guards[currentGuard] = Guard()

    elif(evt.eType == EnumEventType.Asleep):
        assert (currentGuardState == EnumEventType.Wakeup) or (currentGuardState == EnumEventType.Begin), "going to sleep form invalid state"
        currentGuardState = EnumEventType.Asleep
        currentAsleepMinute = evt.date.minute

    elif(evt.eType == EnumEventType.Wakeup):
        assert (currentGuardState == EnumEventType.Asleep), "waking up in invalid state"
        currentGuardState = EnumEventType.Wakeup

        minutesAsleep = evt.date.minute - currentAsleepMinute
        guards[currentGuard].totalMinutesSlept += minutesAsleep
        for i in range(currentAsleepMinute, currentAsleepMinute+minutesAsleep):
            guards[currentGuard].minutesHistogram[i] += 1


maxMinsSlept = -1
maxGuard = -1
maxGuardMaxMinute = -1
for guard in guards:
    maxMinute = guards[guard].minutesHistogram.index(max(guards[guard].minutesHistogram))
    print "Guard #" + guard + " slept " + str(guards[guard].totalMinutesSlept) + " minutes.  ",
    print "Most often slept minute: " + str(maxMinute)
    print "Times slep: " + str(max(guards[guard].minutesHistogram))

    if(guards[guard].totalMinutesSlept > maxMinsSlept):
        maxMinsSlept = guards[guard].totalMinutesSlept
        maxGuard = guard
        maxGuardMaxMinute = maxMinute


print "---------------"
print "Max Guard: " + str(maxGuard)
print "Max Guard Minute: " + str(maxGuardMaxMinute)
print "Checksum = " + str(int(maxGuardMaxMinute) * int(maxGuard))



print "---------------"

maxGuard = -1
maxGuardMinuteWithMax = -1
maxGuardNumTimes = -1
for guard in guards:
    maxCount = max(guards[guard].minutesHistogram)
    minuteWithMax = guards[guard].minutesHistogram.index(maxCount)

    if(maxCount > maxGuardNumTimes):
        maxGuardNumTimes = maxCount 
        maxGuardMinuteWithMax = minuteWithMax
        maxGuard = guard


print "Guard " + str(maxGuard) + " slept " + str(maxGuardNumTimes) + " on minute " + str(maxGuardMinuteWithMax)
print "Checksum = " + str(int(maxGuard) * int(maxGuardMinuteWithMax))










