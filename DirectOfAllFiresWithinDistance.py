__author__ = 'adrianol'


from getCSVStrFromIndex import *
from getCSVValueFromIndex import *
from getDistance import *
from getDirection import *

##################################################################################
def determineDirectOfAllFiresWithinDistance(strFireDataFilenname,
                                            fLatitude,
                                            fLongitude,
                                            fMaximumDistanceInKM):
    listOfNumberOfFiresInEachDirection = dict()
    # make sure we populate the list...
    iCount = 0
    while iCount < 360:
        listOfNumberOfFiresInEachDirection[iCount] = 0
        iCount = iCount + 45

    fhFireData = open(strFireDataFilenname)
    for sALine in fhFireData:
        # Where is the fire?
        if len(sALine) > 0:
            fFireLat       = getLatitude (sALine)
            fFireLong      = getLongitude(sALine)
            fFireMagnitude = getMagnitude(sALine)

            if fFireLat != None and \
                fFireLong != None and \
                fFireMagnitude != None:


                # close?
                fFireDistance = getDistance(fLatitude, fLongitude,
                                            fFireLat,  fFireLong)

                if fFireDistance < fMaximumDistanceInKM * 1000:
                    # What direction is the fire?
                    fFireBearing = getDirection(fLatitude, fLongitude,
                                                fFireLat,  fFireLong)

                    # found to nearest 45degrees
                    iFireBearingRounded = int(fFireBearing / 45.0 + 0.5) * 45

                    if iFireBearingRounded >= 360:
                        iFireBearingRounded = iFireBearingRounded - 360

                    listOfNumberOfFiresInEachDirection[iFireBearingRounded] = \
                        listOfNumberOfFiresInEachDirection.get(iFireBearingRounded, 0) + 1

    listOfNumberOfFiresInEachDirectionSorted = list([(k, v) for k, v in listOfNumberOfFiresInEachDirection.items()])

    listOfNumberOfFiresInEachDirectionSorted.sort(reverse=False)

    return listOfNumberOfFiresInEachDirectionSorted
