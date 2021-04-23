import math


def findupgrades(multiplier, number, nextprice):
    upgrades = -1
    if nextprice == 0:
        return 100
    while upgrades < 100:
        upgrades = upgrades + 1
        now = nextprice - math.floor(multiplier * number ** upgrades)
        if now < 0:
            if -now < nextprice - math.floor(multiplier * number ** (upgrades - 1)):
                return upgrades
            else:
                return upgrades - 1
    return 100


extrinf = int(float(input('How many infinities do you have in extraction? ')))
speedinf = int(float(input('How many infinities do you have in speed? ')))
prodinf = int(float(input('How many infinities do you have in production? ')))
print('For the following questions, answer 0 if maxed.')
chargereq = 1e12 * (0.95 ** findupgrades(25, 1.1, int(float(input('How much does the next charge required upgrade cost? ')))))
speedperc = findupgrades(10, 1.22, int(float(input('How much does the next speed bonus upgrade cost? '))))
prodperc = findupgrades(8, 1.15, int(float(input('How much does the next production bonus upgrade cost? '))))
extrspeed = findupgrades(15, 1.17, int(float(input('How much does the next extraction tick upgrade cost? '))))
speedspeed = findupgrades(30, 1.22, int(float(input('How much does the next speed tick upgrade cost? '))))
prodspeed = findupgrades(10, 1.15, int(float(input('How much does the next production tick upgrade cost? '))))
extrbartime = 31536000 / extrinf * (0.9 ** extrspeed)
extrbarstart = extrbartime
speedbartime = 31536000 / speedinf * (0.9 ** speedspeed)
prodbartime = 31536000 / prodinf * (0.9 ** prodspeed)
speedincrease = 1
prodincrease = 1
extramount = 0.01
extramountstart = extramount
priorextr = extrbartime
priorspeed = speedbartime
priorprod = prodbartime
charge = 0.01
while charge < chargereq:
    while priorspeed <= priorextr:
        while priorprod <= priorspeed:
            prodincrease = prodincrease + prodperc * 0.025 + 0.05
            extramount = prodincrease / 100 + 0.01
            priorprod = priorprod + prodbartime
        priorextr = (priorextr - priorspeed) / (1 + (speedperc * 0.01 + 0.02) / speedincrease) + priorspeed
        speedincrease = speedincrease + 0.01 * (speedperc + 2)
        extrbartime = extrbarstart / speedincrease
        priorspeed = priorspeed + speedbartime
    while priorprod <= priorextr:
        while priorspeed < priorprod:
            priorextr = (priorextr - priorspeed) / (1 + (speedperc * 0.01 + 0.02) / speedincrease) + priorspeed
            speedincrease = speedincrease + 0.01 * (speedperc + 2)
            extrbartime = extrbarstart * speedincrease / 100
            priorspeed = priorspeed + speedbartime
        if priorextr < priorprod:
            break
        prodincrease = prodincrease + prodperc * 0.025 + 0.05
        extramount = prodincrease / 100
        priorprod = priorprod + prodbartime
    charge = charge + extramount
    priorextr = priorextr + extrbartime
timesec = priorextr - extrbartime
print(timesec // 86400, ' days, ', (timesec % 86400) // 3600, ' hours, ', (timesec % 3600) // 60, ' minutes, ', timesec % 60, ' seconds.')
