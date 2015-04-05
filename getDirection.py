
import math
# http://www.sunearthtools.com/tools/distance.php Test Data
def getDirection(zfLat1, zfLong1, zfLat2, zfLong2):
    #http://mathforum.org/library/drmath/view/55417.html
    fLong1 = math.radians(zfLong1)
    fLong2 = math.radians(zfLong2)
    fLat1  = math.radians(zfLat1)
    fLat2  = math.radians(zfLat2)
    y = math.sin(fLong2 - fLong1) * math.cos(fLat2)
    x = math.cos(fLat1) * math.sin(fLat2) - math.sin(fLat1) * math.cos(fLat2) * math.cos(fLong2 - fLong1)
    if y > 0:
        if x > 0:
            tc1 = math.degrees(math.atan(y / x))
        elif x < 0:
            tc1 = 180 - math.degrees(math.atan(-y / x))
        elif x == 0:
            tc1 = 90
    elif y < 0:
        if x > 0:
            tc1 = -math.degrees(math.atan(-y / x))
        elif x < 0:
            tc1 = math.degrees(math.atan(y / x)) - 180
        elif x == 0:
            tc1 = 270
    elif y == 0:
        if x > 0:
            tc1 = 0
        elif x < 0:
            tc1 = 180
            #elif x == 0: the 2 points are the same

    if tc1 < 0:
        tc1 = tc1 + 360

    return tc1


def TestgetDirection():
    fResult = getDirection(0, 98.9407, 0 + 1, 98.9407 + 1)
    if round(fResult, 2) != 45.00:
        return False

    fResult = getDirection(0, 98.9407, 0 + 1, 98.9407 - 1)
    if round(fResult, 2) != -45.00 + 360:
        return False

    fResult = getDirection(0, 98.9407, 0 - 1, 98.9407 + 1)
    if round(fResult, 2) != 135.00:
        return False

    fResult = getDirection(0, 98.9407, 0 - 1, 98.9407 - 1)
    if round(fResult, 2) != -135.00 + 360:
        return False


    fResult = getDirection(0, 98.9407, 0 - 1, 98.9407 + 0)
    if round(fResult, 2) != 180.00:
        return False

    fResult = getDirection(0, 98.9407, 0 + 1, 98.9407 + 0)
    if round(fResult, 2) != 0.00:
        return False

    fResult = getDirection(0, 98.9407, 0 - 0, 98.9407 + 1)
    if round(fResult, 2) != 90.00:
        return False

    fResult = getDirection(0, 98.9407, 0 - 0, 98.9407 - 1)
    if round(fResult, 2) != 270.00:
        return False


    fResult = getDirection(3.55728, -48.12402, 3.33795, -41.99182)
    if round(fResult, 2) != 91.87:
        return False

    return True


