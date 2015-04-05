
##################################################################################
# isFireUnwind - takes wind direction and fire bearing, and works out whether
#                the fire is within a +/- 45 degrees cone upwind
def isFireUpwind(fWindDirection, fFireBearing):
    fDiff = fWindDirection - fFireBearing

    if fDiff < 0:
        fDiff = fDiff + 360
    elif fDiff > 360:
        fDiff = fDiff - 360

    if fDiff > 315 or fDiff < 45:
        return True

    return False

def TestisFireUpwind():
    if isFireUpwind(45, 44) != True:
        return False

    if isFireUpwind(0, -44) != True:
        return False

    if isFireUpwind(180, 190) != True:
        return False    

    if isFireUpwind(180, 170) != True:
        return False  
    

##################################################################################
# bases on distance, wind speed and magnitude, tries to work out whether
# this fire is affecting us
def isFireAffectingUs(fFireMagnitude, fFireDistance, fWindSpeed):

    if fFireDistance < 1000000:
        return True

    return False

