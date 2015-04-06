
#
from getCSVStrFromIndex import *
from getCSVValueFromIndex import *
from getDistance import *
from getDirection import *
from Test import *
from FireHelpers import *
from getWebData import *
from calculateWindVectors import *
from DirectOfAllFiresWithinDistance import *

# Data files download:
# http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ICHIANGM6&day=17&month=3&year=2015&graphspan=day&format=1
# https://earthdata.nasa.gov/data/near-real-time-data/firms/active-fire-data
# https://firms.modaps.eosdis.nasa.gov/active_fire/text/Global_24h.csv
# https://earthdata.nasa.gov/data/near-real-time-data/firms/active-fire-data#tab-content-4

def Main():

    # Definitions
    fGISLatitude            = 18.729000
    fGISLongitude           = 98.940700
    fMaximumDistanceInKM    = 100

    sWeatherDataFilename        = "output/WeatherData.csv"
    sFireDataFilename           = "output/FireData.csv"
    sWindPositionFilename       = "output/WindPosition.dat"
    sNearbyFiresFilename20km    = "output/NearbyFires20km.dat"
    sNearbyFiresFilename100km   = "output/NearbyFires100km.dat"
    sNearbyFiresFilename500km   = "output/NearbyFires500km.dat"

    # First we find the current wind direction
    fWindSpeed           = 0
    fWindDirection       = 0
    iNumberOfFiresUpwind = 0

    #getLatestWebData(sFireDataFilename, sWeatherDataFilename)

    listOfTimeWindDirectionAndDistance = calculateWindVectors(sWeatherDataFilename, fGISLatitude, fGISLongitude)

    #print listOfTimeWindDirectionAndDistance


    WindPositionFilename = open(sWindPositionFilename, "wt")
    for TimeStamp, DirectionDistance in listOfTimeWindDirectionAndDistance:
        WindPositionFilename.write("{0}, {1:d}, {2:d}, {3:d}, {4:d}\n".format(\
            datetime.datetime.fromtimestamp(TimeStamp),\
            int(DirectionDistance[0]), \
            int(DirectionDistance[1]), \
            int(DirectionDistance[2]), \
            int(DirectionDistance[3])))
    WindPositionFilename.close()



    sALine = ""
    fhWeather = open(sWeatherDataFilename)
    for sALine in fhWeather:
        # we want the latest - so keep going until the end
        if len(sALine) > 0:
            fValue = getWindSpeed    (sALine)
            if fValue != None and fValue >= 0:
                fWindSpeed = fValue

            fValue = getWindDirection(sALine)
            if fValue != None and fValue > -361 and fValue <361:
                 fWindDirection = fValue

    # 10km Nearby fires
    listOfNumberOfFiresInEachDirection = determineDirectOfAllFiresWithinDistance(sFireDataFilename,\
                                            fGISLatitude,
                                            fGISLongitude,
                                            20)

    NearbyFiresFilename = open(sNearbyFiresFilename20km, "wt")
    for Direction, Count in listOfNumberOfFiresInEachDirection:
        NearbyFiresFilename.write("{0:d}, {1:d}\n".format(Direction, Count))
    NearbyFiresFilename.close()

    # 100km Nearby fires
    listOfNumberOfFiresInEachDirection = determineDirectOfAllFiresWithinDistance(sFireDataFilename,\
                                            fGISLatitude,
                                            fGISLongitude,
                                            100)

    NearbyFiresFilename = open(sNearbyFiresFilename100km, "wt")
    for Direction, Count in listOfNumberOfFiresInEachDirection:
        NearbyFiresFilename.write("{0:d}, {1:d}\n".format(Direction, Count))
    NearbyFiresFilename.close()

    # 100km Nearby fires
    listOfNumberOfFiresInEachDirection = determineDirectOfAllFiresWithinDistance(sFireDataFilename,\
                                            fGISLatitude,
                                            fGISLongitude,
                                            500)

    NearbyFiresFilename = open(sNearbyFiresFilename500km, "wt")
    for Direction, Count in listOfNumberOfFiresInEachDirection:
        NearbyFiresFilename.write("{0:d}, {1:d}\n".format(Direction, Count))
    NearbyFiresFilename.close()


    for Direction, Count in listOfNumberOfFiresInEachDirection:
        NearbyFiresFilename.write("{0:3d} - {1:6d} fires within {2:d}km\n".format(Direction, Count, fMaximumDistanceInKM))


    # now check the fire data
    fhFireData = open(sFireDataFilename)
    for sALine in fhFireData:
        # Where is the fire?
        if len(sALine) > 0:
            fFireLat       = getLatitude (sALine)
            fFireLong      = getLongitude(sALine)
            fFireMagnitude = getMagnitude(sALine)

            if fFireLat != None and \
                fFireLong != None and \
                fFireMagnitude != None:
                # What direction is the fire?
                fFireBearing = getDirection(fGISLatitude, fGISLongitude,\
                                            fFireLat,     fFireLong)

                # Is the fire upwind?
                if isFireUpwind(fWindDirection, fFireBearing):
                    # Yes - how close is the fire?
                    fFireDistance = getDistance(fGISLatitude, fGISLongitude,\
                                                fFireLat,     fFireLong)

                    # Is this fire affecting us?
                    if isFireAffectingUs(fFireMagnitude, fFireDistance, fWindSpeed):
                        iNumberOfFiresUpwind = iNumberOfFiresUpwind + 1

    print "Total number of fires affecting us:", iNumberOfFiresUpwind

Main()
