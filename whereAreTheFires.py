
#
from getCSVStrFromIndex import *
from getCSVValueFromIndex import *
from getDistance import *
from getDirection import *
from Test import *
from FireHelpers import *
from getWebData import *


# Data files download:
# http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ICHIANGM6&day=17&month=3&year=2015&graphspan=day&format=1
# https://earthdata.nasa.gov/data/near-real-time-data/firms/active-fire-data
# https://firms.modaps.eosdis.nasa.gov/active_fire/text/Global_24h.csv
# https://earthdata.nasa.gov/data/near-real-time-data/firms/active-fire-data#tab-content-4

def Main():

    # Definitions
    fGISLatitude  = 18.729000
    fGISLongitude = 98.940700

    # First we find the current wind direction
    fWindSpeed           = 0
    fWindDirection       = 0
    iNumberOfFiresUpwind = 0

    getLatestWebData()

    sALine = ""
    fhWeather = open("WeatherData.csv")
    for sALine in fhWeather:
        # we want the latest - so keep going until the end
        if len(sALine) > 0:
            fValue = getWindSpeed    (sALine)
            if fValue != None and fValue >= 0:
                fWindSpeed = fValue

            fValue = getWindDirection(sALine)
            if fValue != None and fValue > -361 and fValue <361:
                 fWindDirection = fValue


    # now check the fire data
    fhFireData = open("FireData.csv")
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
