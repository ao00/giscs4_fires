# finds the distance between 2 given latitude&longitude coordinates
import math

# http://www.sunearthtools.com/tools/distance.php

def deg2rad(fDeg):
    return fDeg * (math.pi / 180.0)


def rad2deg(fRad):
    return fRad * (180.0 / math.pi)


def getDistance(zfLat1, zfLong1, zfLat2, zfLong2):
    fLong1 = math.radians(zfLong1)
    fLong2 = math.radians(zfLong2)
    fLat1  = math.radians(zfLat1)
    fLat2  = math.radians(zfLat2)

    theta = fLong1 - fLong2

    dist = math.sin(fLat1) * math.sin(fLat2) + \
           math.cos(fLat1) * math.cos(fLat2) * \
           math.cos(theta)

    dist1 = math.acos(dist)

    dist2 = rad2deg(dist1)

    meters1 = (dist2 * 111.18957696 * 1000.0)

    meters2 = (dist1 * 6372796.0)

    return meters2

def TestgetDistance():
    fResult = getDistance(40.76, -73.984, 45.20138, -69.59784)
    if round(fResult, 2) != 609227.56:
        return False

    return True
    
