

def isFireUpwind(fWindDirection, fFireBearing):
    fDiff = fWindDirection - fFireBearing

    if fDiff < 0:
        fDiff = fDiff + 360
    elif fDiff > 360:
        fDiff = fDiff - 360

    if fDiff > -45 and fDiff < 45:
        return True

    return False



def isFireAffectingUs(fFireMagnitude, fFireDistance, fWindSpeed):

    if fFireDistance < 1000000:
        return True

    return False
