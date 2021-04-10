import math


def findupgrades(multiplier, number, nextprice):
    cost = 0
    upgrades = -1
    if nextprice == 0:
        return 100
    while cost < nextprice:
        upgrades = upgrades + 1
        cost = math.floor(multiplier * number ** upgrades)
        if upgrades == 100:
            return upgrades
        if cost == nextprice:
            return upgrades


extrinf = int(input('How many infinities do you have in extraction? '))
speedinf = int(input('How many infinities do you have in speed? '))
prodinf = int(input('How many infinities do you have in production? '))
print('For the following questions, answer 0 if maxed.')
chargereq = 1e12 * (0.95 ** findupgrades(25, 1.1, int(input('How much does the next charge required upgrade cost? '))))
speedperc = findupgrades(10, 1.22, int(input('How much does the next speed bonus upgrade cost? ')))
prodperc = findupgrades(8, 1.15, int(input('How much does the next production bonus upgrade cost? ')))
extrspeed = findupgrades(15, 1.17, int(input('How much does the next extraction duration upgrade cost? ')))
speedspeed = findupgrades(30, 1.22, int(input('How much does the next speed duration upgrade cost? ')))
prodspeed = findupgrades(10, 1.15, int(input('How much does the next production duration upgrade cost? ')))
extrbartime = round(31536000 / extrinf * (0.9 ** extrspeed), 15)
extrbarstart = extrbartime
speedbartime = round(31536000 / speedinf * (0.9 ** speedspeed), 15)
prodbartime = round(31536000 / prodinf * (0.9 ** prodspeed), 15)
speedincrease = 1.01
extramount = 0.01
priorextr = extrbartime
priorspeed = speedbartime
priorprod = prodbartime
charge = 0
while charge < chargereq:
    while priorspeed < priorextr:
        speedincrease = speedincrease + 0.01 * speedperc
        priorextr = (priorextr - priorspeed) / (speedperc * 0.01 + 1) + priorspeed
        extrbartime = extrbarstart / speedincrease
        priorspeed = priorspeed + speedbartime 
    while priorprod < priorextr:
        extramount = extramount + round(0.01 * (1.05 + 0.025 * prodperc), 3)
        priorprod = priorprod + prodbartime
    charge = charge + extramount
    priorextr = priorextr + extrbartime
timesecspeed = priorspeed - speedbartime
timesecprod = priorprod - prodbartime
if timesecprod > timesecspeed:
    timesec = timesecprod
else:
    timesec = timesecspeed
days = timesec // 86400
timesec = timesec % 86400
hours = timesec // 3600
timesec = timesec % 3600
minutes = timesec // 60
timesec = timesec % 60
print(days, ' days, ', hours, ' hours, ', minutes, ' minutes, ', timesec, ' seconds.')
