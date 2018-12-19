#!/usr/bin/python
'''
reg0 = 0
reg1 = 860
reg2 = 1
reg3 = 1

while reg3 <= reg1:
    reg2 = 1
    print "here"
    while reg2 <= reg1:
        #print "{0:3} {1:3}".format(reg2, reg3)

        if (reg3 * reg2) == reg1:
            reg0 += reg3

        reg2+=1
    reg3 += 1

print reg0
'''

reg0 = 0
#reg1 = 860
reg1 = 10551260
reg2 = 1
reg3 = 1

while reg3 <= reg1:
    reg2 = 1
    #while reg2 <= reg1:
        #print "{0:3} {1:3}".format(reg2, reg3)

        #if (reg3 * reg2) == reg1:
        #    reg0 += reg3

        #reg2+=1

    if reg1 % reg3 == 0:
        reg0 += reg3

    reg3 += 1

print reg0