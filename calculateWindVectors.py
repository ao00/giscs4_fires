__author__ = 'adrianol'

import time
import datetime
from getCSVStrFromIndex import *
from getCSVValueFromIndex import *
from getNewPosition import *
from getDistance import *
from getDirection import *

def calculateWindVectors(strWeatherDataFilenname,\
                         fLatitudeStart,
                         fLongitudeStart):
    # returns a dictionary of direction and distance
    # create a list, then we reverse the list, and work out accumulative vectors

    try:
        fhWeather = open(strWeatherDataFilenname)

        sALine = ""
        listTimeDirectionSpeed = dict()

        for sALine in fhWeather:
            # we want the latest - so keep going until the end
            if len(sALine) > 0:
                fWindSpeed = getWindSpeed(sALine)

                if fWindSpeed != None and fWindSpeed >= 0:
                    fWindDirection = getWindDirection(sALine)

                    if fWindDirection != None and fWindDirection > -361 and fWindDirection < 361:
                        strTimeStamp = getWeatherTimeStamp(sALine)

                        if strTimeStamp != None:
                            # time to process...
                            TimeStamp = time.mktime(time.strptime(strTimeStamp, '%Y-%m-%d %H:%M:%S'))

                            listTimeDirectionSpeed[TimeStamp] = [fWindDirection, fWindSpeed]

        #print listTimeDirectionSpeed

        TimeDirectionSpeedSorted = list([(k, v) for k, v in listTimeDirectionSpeed.items()])

        TimeDirectionSpeedSorted.sort(reverse=True)

        listTimeDirectionSpeed.clear()

        tmCurrentTime = time.time()
        fLatitude  = fLatitudeStart
        fLongitude = fLongitudeStart
        fBearing   = 0
        fDistance  = 0

        for TimeStamp, WindDirectionAndSpeed in TimeDirectionSpeedSorted:

            if WindDirectionAndSpeed[1] > 0:
                tmTimeDiff = tmCurrentTime - TimeStamp

                fDistance = WindDirectionAndSpeed[1] * tmTimeDiff / 60.0 / 60.0

                NewPosition = getNewPositionFromDistanceAndDirection(fLatitude, \
                                                                     fLongitude, \
                                                                     WindDirectionAndSpeed[0], \
                                                                     fDistance)

                fLatitude  = NewPosition['Latitude']
                fLongitude = NewPosition['Longitude']

                fBearing  = getDirection(fLatitudeStart, fLongitudeStart,\
                                        fLatitude, fLongitude)

                fDistance = getDistance(fLatitudeStart, fLongitudeStart,\
                                        fLatitude, fLongitude)

            listTimeDirectionSpeed[TimeStamp] = [fBearing, fDistance]

            tmCurrentTime   = TimeStamp

        #print TimeDirectionSpeedSorted

        TimeDirectionSpeedSorted = list([(k, v) for k, v in listTimeDirectionSpeed.items()])

        TimeDirectionSpeedSorted.sort(reverse=True)

        return TimeDirectionSpeedSorted
    except:
        return None
