x = 0x39f737
y = 0x10000

print "{} {}".format(hex(x),hex(y))

pastXs=[]

numMatches=0
for i in range(100000):
    while True:
        x = (((x + y %256) & 0xffffff) * 65899) & 0xffffff
        if y < 256: break
        y = y>>8


    matches=False
    for oldX in pastXs:
        if oldX==x:
            matches=True
            numMatches+=1

    print "{} {}".format(hex(x), matches)

    pastXs.append(x)
    y = x | 0x10000
    x = 0x39f737

    if numMatches > 10: break
