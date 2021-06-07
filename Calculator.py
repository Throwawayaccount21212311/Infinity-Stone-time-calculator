#!/usr/bin/env python3

import math
import time

def findupgrades(multiplier, base, nextprice):
    if nextprice == 0:
        return 100
    upgrades = -1
    while upgrades < 100:
        upgrades += 1
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
fps = int(input('Average FPS: '))
print('For the following questions, answer 0 if maxed.')
chargereq = 1e12 * (0.95 ** findupgrades(25, 1.1, int(float(input('How much does the next charge required upgrade cost? ')))))
speedperc = findupgrades(10, 1.22, int(float(input('How much does the next speed bonus upgrade cost? ')))) * 0.01 + 0.02
prodperc = findupgrades(8, 1.15, int(float(input('How much does the next production bonus upgrade cost? ')))) * 0.025 + 0.05
extrspeed = findupgrades(15, 1.17, int(float(input('How much does the next extraction tick upgrade cost? '))))
speedspeed = findupgrades(30, 1.22, int(float(input('How much does the next speed tick upgrade cost? '))))
prodspeed = findupgrades(10, 1.15, int(float(input('How much does the next production tick upgrade cost? '))))
if speedinf < 1:
    speedbartime = 1.7e308
else:
    speedbartime = 31536000 / speedinf * (0.9 ** speedspeed)
if prodinf < 1:
    prodbartime = 1.7e308
else:
    prodbartime = 31536000 / prodinf * (0.9 ** prodspeed)
extrbartime = 31536000 / extrinf * (0.9 ** extrspeed)
extrbarstart = extrbartime
speedincrease = 1
extramount = 0.01
speedcounter = 1
counter = 0
timeextr = extrbartime
timespeed = speedbartime
timeprod = prodbartime
charge = 0.01
countperc = 1
deltatime = 1 / fps
timestamp = time.process_time()
while charge < chargereq:
    prodcheck = (deltatime - timeprod) // prodbartime
    while prodcheck > 1:
        extramount = prodperc / 100 * prodcheck + extramount
        timeprod += prodbartime * prodcheck
    while (deltatime - timespeed) / speedbartime > 1:
        speedincrease = speedincrease + speedperc
        if speedcounter == 1:
            timeextr = (timeextr - timespeed) / (1 + speedperc) + timespeed
            counter = 0
        else:
            timeextr = (timeextr - timespeed) * (((speedincrease - 1) / speedperc - 1) / ((speedincrease - 1) / speedperc)) + timespeed
        extrbartime = extrbarstart / speedincrease
        timespeed += speedbartime
    extrcheck = (deltatime - timeextr) // extrbartime
    if extrcheck > 1:
        charge = charge + extramount * extrcheck
        timeextr += extrbartime * extrcheck
    deltatime += 1 / fps
    counter += 1
    if (charge / chargereq) ** (1 / 3) * 100 > countperc:
        timeleft = int(time.process_time() - timestamp * (100 / countperc))
        print('{0}% completed. Expected time left- ~~{1}:{2}:{3}'.format(round((charge / chargereq), 1) ** (1 / 3) * 100, timeleft // 86400, timeleft % 3600 // 60, timeleft % 60))
        countperc = round(countperc + 0.1, 1)
timesec = deltatime - 1 / fps
print(extramount, speedincrease * 100)
print('{0} days, {1} hours, {2} minutes, {3} seconds'.format(timesec // 86400, timesec % 86400 // 3600, timesec % 3600 // 60, timesec % 60))
input('\nPress ENTER to exit: ')
