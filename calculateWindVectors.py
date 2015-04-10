__author__ = 'adrianol'

import time
import datetime
from getCSVStrFromIndex import *
from getCSVValueFromIndex import *
from getNewPosition import *
from getDistance import *
from getDirection import *

def calculateWindVectors(strWeatherDataFilename,
                         fLatitudeStart,
                         fLongitudeStart):
    # returns a dictionary of direction and distance
    # create a list, then we reverse the list, and work out accumulative vectors

    try:
        fhWeather = open(strWeatherDataFilename)

        sALine = ""
        listTimeDirectionSpeed = dict()

        for sALine in fhWeather:
            # we want the latest - so keep going until the end
            if len(sALine) > 0:
                strTimeStamp = getWeatherTimeStamp(sALine)

                if strTimeStamp != None and len(strTimeStamp) > 5:

                    try:
                        TimeStamp = time.mktime(time.strptime(strTimeStamp, '%Y-%m-%d %H:%M:%S'))

                        fWindSpeed = getWindSpeed(sALine)

                        if fWindSpeed != None and fWindSpeed >= 0:
                            fWindDirection = getWindDirection(sALine)

                            if fWindDirection != None and fWindDirection > -361 and fWindDirection < 361:
                                # check that there is also a valid temperature
                                fTemperature = getWeatherTemperature(sALine)

                                if fTemperature != None and fTemperature > -100:    # good...
                                    # time to process...
                                    listTimeDirectionSpeed[TimeStamp] = [fWindDirection, fWindSpeed]
                                else:
                                    listTimeDirectionSpeed[TimeStamp] = [0, 0]
                            else:
                                listTimeDirectionSpeed[TimeStamp] = [0, 0]
                        else:
                            listTimeDirectionSpeed[TimeStamp] = [0, 0]
                    except:
                        # keep going...
                        TimeStamp = None

        #print listTimeDirectionSpeed
        #for TimeStamp, DirectionDistance in listTimeDirectionSpeed.items():
        #    print "{0}, {1:d}, {2:d}".format(\
        #            datetime.datetime.fromtimestamp(TimeStamp),\
        #            int(DirectionDistance[0]), \
        #            int(DirectionDistance[1]))

        TimeDirectionSpeedSorted = list([(k, v) for k, v in listTimeDirectionSpeed.items()])

        TimeDirectionSpeedSorted.sort(reverse=True)

        #print TimeDirectionSpeedSorted
        #for TimeStamp, DirectionDistance in TimeDirectionSpeedSorted:
        #    print "{0}, {1:d}, {2:d}".format(\
        #            datetime.datetime.fromtimestamp(TimeStamp),\
        #            int(DirectionDistance[0]), \
        #            int(DirectionDistance[1]))

        listTimeDirectionSpeed.clear()

        tmCurrentTime = None
        fLatitude  = fLatitudeStart
        fLongitude = fLongitudeStart
        fBearing   = 0
        fDistance  = 0

        for TimeStamp, WindDirectionAndSpeed in TimeDirectionSpeedSorted:

            if WindDirectionAndSpeed[1] > 0:
                if tmCurrentTime == None:
                    tmCurrentTime = TimeStamp
                tmTimeDiff = tmCurrentTime - TimeStamp

                fDistance = WindDirectionAndSpeed[1] * tmTimeDiff / 60.0 / 60.0

                NewPosition = getNewPositionFromDistanceAndDirection(fLatitude,
                                                                     fLongitude,
                                                                     WindDirectionAndSpeed[0],
                                                                     fDistance)

                fLatitude  = NewPosition['Latitude']
                fLongitude = NewPosition['Longitude']

                fBearing  = getDirection(fLatitudeStart, fLongitudeStart,
                                        fLatitude, fLongitude)

                fDistance = getDistance(fLatitudeStart, fLongitudeStart,
                                        fLatitude, fLongitude)

            listTimeDirectionSpeed[TimeStamp] = [fBearing, fDistance, WindDirectionAndSpeed[0], WindDirectionAndSpeed[1]]

            tmCurrentTime   = TimeStamp

        #print TimeDirectionSpeedSorted

        TimeDirectionSpeedSorted = list([(k, v) for k, v in listTimeDirectionSpeed.items()])

        TimeDirectionSpeedSorted.sort(reverse=True)

        return TimeDirectionSpeedSorted
    except:
        return None


def findWindVectorForLast24Hours(listOfTimeWindDirectionAndDistance):
    try:
        # find first entry - that is NOW...
        tmStartTime = None

        for tmTimeStamp, DirectionDistance in listOfTimeWindDirectionAndDistance:
            if tmStartTime == None:
                tmStartTime = tmTimeStamp
            else:
                tmTimeDiff = tmStartTime - tmTimeStamp

                if tmTimeDiff >= 24 * 60 * 60:
                    return [tmTimeStamp, DirectionDistance[0], DirectionDistance[1]]


        return None

    except:
        return None