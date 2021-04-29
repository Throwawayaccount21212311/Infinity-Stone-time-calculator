#!/usr/bin/env python3

import math


def findupgrades(multiplier, base, nextprice):
    upgrades = -1
    if nextprice == 0:
        return 100
    while upgrades < 100:
        upgrades = upgrades + 1
        now = nextprice - math.floor(multiplier * base ** upgrades)
        if now < 0:
            if -now < nextprice - math.floor(multiplier * base ** (upgrades - 1)):
                return upgrades
            else:
                return upgrades - 1
    return 100


extrinf = int(float(input('How many infinities do you have in extraction? ')))
speedinf = int(float(input('How many infinities do you have in speed? ')))
prodinf = int(float(input('How many infinities do you have in production? ')))
print('For the following questions, answer 0 if maxed.')
chargereq = 1e12 * (0.95 ** findupgrades(25, 1.1, int(float(input('How much does the next charge required upgrade cost? ')))))
speedperc = findupgrades(10, 1.22, int(float(input('How much does the next speed bonus upgrade cost? ')))) * 0.01 + 0.02
prodperc = findupgrades(8, 1.15, int(float(input('How much does the next production bonus upgrade cost? ')))) * 0.025 + 0.05
extrspeed = findupgrades(15, 1.17, int(float(input('How much does the next extraction tick upgrade cost? '))))
speedspeed = findupgrades(30, 1.22, int(float(input('How much does the next speed tick upgrade cost? '))))
prodspeed = findupgrades(10, 1.15, int(float(input('How much does the next production tick upgrade cost? '))))
extrbartime = 31536000 / extrinf * (0.9 ** extrspeed)
extrbarstart = extrbartime
if speedinf < 1:
    speedbartime = 1.7e308
else:
    speedbartime = 31536000 / speedinf * (0.9 ** speedspeed)
if prodinf < 1:
    prodbartime = 1.7e308
else:
    prodbartime = 31536000 / prodinf * (0.9 ** prodspeed)
speedincrease = 1
extramount = 0.01
counter = 1
timeextr = extrbartime
timespeed = speedbartime
timeprod = prodbartime
charge = 0.01
while charge < chargereq:
    while timespeed <= timeextr:
        while timeprod <= timespeed:
            extramount = prodperc / 100 + extramount
            timeprod = timeprod + prodbartime
        speedincrease = speedincrease + speedperc
        if counter == 1:
            timeextr = (timeextr - timespeed) / (1 + speedperc) + timespeed
            counter = 0
        else:
            timeextr = (timeextr - timespeed) * (((speedincrease - 1) / speedperc - 1) / ((speedincrease - 1) / speedperc)) + timespeed
        extrbartime = extrbarstart / speedincrease
        timespeed = timespeed + speedbartime
    while timeprod <= timeextr:
        extramount = prodperc / 100 + extramount
        timeprod = timeprod + prodbartime
    charge = charge + extramount
    timeextr = timeextr + extrbartime
timesec = timeextr - extrbartime
print(timesec // 86400, 'days,', (timesec % 86400) // 3600, 'hours,', (timesec % 3600) // 60, 'minutes,', timesec % 60, 'seconds.')
