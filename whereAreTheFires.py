
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
from getLatestAQDailyAverage import *

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

    sWeatherDataFilename            = "output/WeatherData.csv"
    sFireDataFilename               = "output/FireData.csv"
    sWindPositionFilename           = "output/WindPosition.dat"
    sDailyWindPositionFilename      = "output/WindPositionDaily.dat"
    sNearbyFiresFilename20km        = "output/NearbyFires20km.dat"
    sNearbyFiresFilename100km       = "output/NearbyFires100km.dat"
    sNearbyFiresFilename200km       = "output/NearbyFires200km.dat"
    sNearbyFiresFilename500km       = "output/NearbyFires500km.dat"
    sAirQualityDailyAveragesLatest  = "output/AQDailyAveragesLatest.dat"
    sAirQualityDailyAverages        = "output/AQDailyAverages.dat"

    # First we find the current wind direction
    fWindSpeed           = 0
    fWindDirection       = 0
    iNumberOfFiresUpwind = 0

    print "Downloading latest data"
    getLatestWebData(sFireDataFilename, sWeatherDataFilename, sAirQualityDailyAveragesLatest)


    # Get AirQuality average
    print "Extracting latest AirQuality"
    latestAQDailyAverage = getLatestAQDailyAverage(sAirQualityDailyAveragesLatest)
    if latestAQDailyAverage != None:
        DailyAQFilename = open(sAirQualityDailyAverages, "at")

        DailyAQFilename.write("{0}, {1:d}, {2:d}\n".format(
            datetime.datetime.fromtimestamp(latestAQDailyAverage[0]),
            int(latestAQDailyAverage[1]),
            int(latestAQDailyAverage[2])))
        DailyAQFilename.close()


    # Get Wind Vectors
    print "Calculating wind vector"
    listOfTimeWindDirectionAndDistance = calculateWindVectors(sWeatherDataFilename, fGISLatitude, fGISLongitude)

    #print listOfTimeWindDirectionAndDistance

    WindPositionFilename = open(sWindPositionFilename, "wt")
    for TimeStamp, DirectionDistance in listOfTimeWindDirectionAndDistance:
        WindPositionFilename.write("{0}, {1:d}, {2:d}, {3:d}, {4:d}\n".format(
            datetime.datetime.fromtimestamp(TimeStamp),
            int(DirectionDistance[0]),
            int(DirectionDistance[1]),
            int(DirectionDistance[2]),
            int(DirectionDistance[3])))
    WindPositionFilename.close()

    WindVectorForLast24Hours = findWindVectorForLast24Hours(listOfTimeWindDirectionAndDistance)

    if WindVectorForLast24Hours != None:
        DailyWindPositionFilename = open(sDailyWindPositionFilename, "at")

        DailyWindPositionFilename.write("{0}, {1:d}, {2:d}\n".format(
            datetime.datetime.fromtimestamp(WindVectorForLast24Hours[0]),
            int(WindVectorForLast24Hours[1]),
            int(WindVectorForLast24Hours[2])))
        DailyWindPositionFilename.close()



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
    print "Determining fires within 20km radius"
    listOfNumberOfFiresInEachDirection = determineDirectOfAllFiresWithinDistance(sFireDataFilename,\
                                            fGISLatitude,
                                            fGISLongitude,
                                            20)

    NearbyFiresFilename = open(sNearbyFiresFilename20km, "at")
    NearbyFiresFilename.write("{0}, ".format(datetime.datetime.now()))
    for Direction, Count in listOfNumberOfFiresInEachDirection:
        NearbyFiresFilename.write("{0:d}, {1:d}, ".format(Direction, Count))
    NearbyFiresFilename.write("\n")
    NearbyFiresFilename.close()


    # 100km Nearby fires
    print "Determining fires within 100km radius"
    listOfNumberOfFiresInEachDirection = determineDirectOfAllFiresWithinDistance(sFireDataFilename,\
                                            fGISLatitude,
                                            fGISLongitude,
                                            100)

    NearbyFiresFilename = open(sNearbyFiresFilename100km, "at")
    NearbyFiresFilename.write("{0}, ".format(datetime.datetime.now()))
    for Direction, Count in listOfNumberOfFiresInEachDirection:
        NearbyFiresFilename.write("{0:d}, {1:d}, ".format(Direction, Count))
    NearbyFiresFilename.write("\n")
    NearbyFiresFilename.close()


    # 200km Nearby fires
    print "Determining fires within 200km radius"
    listOfNumberOfFiresInEachDirection = determineDirectOfAllFiresWithinDistance(sFireDataFilename,\
                                            fGISLatitude,
                                            fGISLongitude,
                                            200)

    NearbyFiresFilename = open(sNearbyFiresFilename200km, "at")
    NearbyFiresFilename.write("{0}, ".format(datetime.datetime.now()))
    for Direction, Count in listOfNumberOfFiresInEachDirection:
        NearbyFiresFilename.write("{0:d}, {1:d}, ".format(Direction, Count))
    NearbyFiresFilename.write("\n")
    NearbyFiresFilename.close()


    # 500km Nearby fires
    print "Determining fires within 500km radius"
    listOfNumberOfFiresInEachDirection = determineDirectOfAllFiresWithinDistance(sFireDataFilename,\
                                            fGISLatitude,
                                            fGISLongitude,
                                            500)

    NearbyFiresFilename = open(sNearbyFiresFilename500km, "at")
    NearbyFiresFilename.write("{0}, ".format(datetime.datetime.now()))
    for Direction, Count in listOfNumberOfFiresInEachDirection:
        NearbyFiresFilename.write("{0:d}, {1:d}, ".format(Direction, Count))
    NearbyFiresFilename.write("\n")
    NearbyFiresFilename.close()



    #for Direction, Count in listOfNumberOfFiresInEachDirection:
    #    NearbyFiresFilename.write("{0:3d} - {1:6d} fires within {2:d}km\n".format(Direction, Count, fMaximumDistanceInKM))


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
