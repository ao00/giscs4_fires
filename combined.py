###############################################################################
# Combination of all project files to allow running under codeskulptor
#
# You can also run this as is in
# http://www.tutorialspoint.com/execute_python_online.php
###############################################################################
# imports
import math


###############################################################################
# csv
# Function: getCSVStrFromIndex(zi, zstrCSV)
# Parameters: zi = index (zi = 0 for first value), zstrCSV = line of CSV data
# Return: strValue (the string in the CSV at index zi)
# Description: Extract string value from a line of CSV data using index
def getCSVStrFromIndex(zi, zstrCSV):
    try:
        strResults = zstrCSV.split(",")[zi]
        return strResults
    except:
        return ""

    


###############################################################################
# values from csv
def getCSVIntFromIndex(zi, zstrCSV):
    strCSV = getCSVStrFromIndex(zi, zstrCSV);
    try:
        if len(strCSV) == 0:
            return None
        iCSV = int(strCSV)
    except:
        return None
    return iCSV


def getCSVFloatFromIndex(zi, zstrCSV):
    strCSV = getCSVStrFromIndex(zi, zstrCSV);
    try:
        if len(strCSV) == 0:
            return None
        floatCSV = float(strCSV)
    except:
        return None
    return floatCSV
    
###############################################################################
# https://firms.modaps.eosdis.nasa.gov/active_fire/text/Global_48h.csv
# http://pw.ajosoft.com/pwglobalfires48h.php
# latitude,longitude,brightness,scan,track,acq_date,acq_time,satellite,confidence,version,bright_t31,frp
# -13.501,-172.57,311.5,3,1.6,2015-03-29, 0040,A,33,5.0       ,292.6,45.5
# -13.498,-172.55,312.7,3,1.6,2015-03-29, 0040,A,42,5.0       ,293.4,50.7


#Fire Data
def getLatitude(zstrFireCSV):
    return getCSVFloatFromIndex(0, zstrFireCSV)


def getLongitude(zstrFireCSV):
    return getCSVFloatFromIndex(1, zstrFireCSV)


def getMagnitude(zstrFireCSV):
    return getCSVFloatFromIndex(2, zstrFireCSV)

#Wind Data
def getWindSpeed(zstrWeatherCSV):
    return getCSVFloatFromIndex(6, zstrWeatherCSV)


def getWindDirection(zstrWeatherCSV):
    return getCSVIntFromIndex(5, zstrWeatherCSV)


###############################################################################
# direction
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
    return tc1


##############################################################################
# distance

# finds the distance between 2 given latitude&longitude coordinates

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
    
    #metersAverage uses an average volumetric radius
    metersAverage = (dist2 * 111.18957696 * 1000.0)
    
    #metersSiam uses a specific radius to Siam's latitude
    metersSiam = (dist1 * 6372796.0)

    return metersSiam

###############################################################################
# other helper functions


def isFireUpwind(fWindDirection, fFireBearing):
    fDiff = fWindDirection - fFireBearing

    if fDiff < 0:
        fDiff = fDiff + 360
    elif fDiff > 360:
        fDiff = fDiff - 360

    if fDiff > 315 or fDiff < 45:
        return True

    return False



def isFireAffectingUs(fFireMagnitude, fFireDistance, fWindSpeed):

    if fFireDistance < 1000000:
        return True

    return False
    
    
###############################################################################
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

#Time,TemperatureC,DewpointC,PressurehPa,WindDirection,WindDirectionDegrees,WindSpeedKMH,WindSpeedGustKMH,Humidity,HourlyPrecipMM,Conditions,Clouds,dailyrainMM,SoftwareType,DateUTC
    lstWeatherData = [\
"2015-03-24 00:04:00,26.0,18.4,1010.0,North,-9999,0.0,0.0,63,0.0,,,-2539.7,weewx-3.1.0,2015-03-23 17:04:00,",\
"2015-03-24 00:09:00,26.0,18.4,1010.0,North,-9999,0.0,0.0,63,0.0,,,-2539.7,weewx-3.1.0,2015-03-23 17:09:00,",\
"2015-03-24 00:14:00,25.9,18.6,1010.0,North,-9999,0.0,0.0,64,0.0,,,-2539.7,weewx-3.1.0,2015-03-23 17:14:00,",\
"2015-03-24 00:19:00,25.9,18.8,1010.0,North,-9999,0.0,0.0,65,0.0,,,-2539.7,weewx-3.1.0,2015-03-23 17:19:00,",\
"2015-03-24 00:24:00,25.9,18.6,1010.0,North,-9999,0.0,0.0,64,0.0,,,-2539.7,weewx-3.1.0,2015-03-23 17:24:00,",\
"2015-03-24 00:29:00,25.8,18.7,1010.0,North,-9999,0.0,0.0,65,0.0,,,-2539.7,weewx-3.1.0,2015-03-23 17:29:00,",\
"2015-03-24 00:34:00,25.8,18.7,1010.0,North,-9999,0.0,0.0,65,0.0,,,0.0,weewx-3.1.0,2015-03-23 17:34:00,",\
"2015-03-24 00:39:00,-573.3,-73.3,-3386.0,North,-9999,-1608.8,-1607.4,-999,0.0,,,0.0,weewx-3.1.0,2015-03-23 17:39:00,",\
"2015-03-24 00:44:00,-573.3,-73.3,-3386.0,North,-9999,-1608.8,-1607.4,-999,0.0,,,0.0,weewx-3.1.0,2015-03-23 17:44:00,",\
"2015-03-24 00:49:00,-573.3,-73.3,-3386.0,North,-9999,-1608.8,-1607.4,-999,0.0,,,0.0,weewx-3.1.0,2015-03-23 17:49:00, "\
]

#latitude,longitude,brightness,scan,track,acq_date,acq_time,satellite,confidence,version,bright_t31,frp
    lstFireData = [\
"19.924,97.482,314.9,4.4,1.9,2015-03-21, 0325,T,54,5.0       ,304.1,49",\
"19.282,100.96,312.6,2.4,1.5,2015-03-21, 0325,T,55,5.0       ,296.7,25",\
"19.218,101.048,321.5,2.3,1.5,2015-03-21, 0325,T,74,5.0       ,295.7,61.1",\
"19.36,99.369,314.7,3.1,1.7,2015-03-21, 0325,T,8,5.0       ,297.2,46.9",\
"19.388,98.91,322.9,3.4,1.7,2015-03-21, 0325,T,76,5.0       ,300.9,110.5",\
"19.392,98.906,322.8,3.4,1.7,2015-03-21, 0325,T,76,5.0       ,300.2,113.7",\
"19.347,99.362,321.7,3.1,1.7,2015-03-21, 0325,T,74,5.0       ,298.6,93.4",\
"19.143,101.031,325.1,2.3,1.5,2015-03-21, 0325,T,78,5.0       ,295.1,81.1",\
"19.132,101.008,337.5,2.3,1.5,2015-03-21, 0325,T,88,5.0       ,294.8,144",\
"19.129,101.034,325.4,2.3,1.5,2015-03-21, 0325,T,79,5.0       ,294.4,82.7",\
"19.122,101.002,323,2.3,1.5,2015-03-21, 0325,T,76,5.0       ,295.2,71.5",\
"19.119,101.025,323,2.3,1.5,2015-03-21, 0325,T,76,5.0       ,294.8,73.7",\
"19.318,97.614,313,4.2,1.9,2015-03-21, 0325,T,42,5.0       ,301.6,60.9",\
"19.19,97.043,326.1,4.6,2,2015-03-21, 0325,T,79,5.0       ,302.5,191.1",\
"19.191,97.037,323,4.6,2,2015-03-21, 0325,T,76,5.0       ,302.5,166.3",\
"19.187,97.082,317.4,4.6,2,2015-03-21, 0325,T,68,5.0       ,303.5,96.7",\
"19.173,97.031,329.1,4.6,2,2015-03-21, 0325,T,82,5.0       ,302.1,232.7",\
"19.174,97.026,326.7,4.6,2,2015-03-21, 0325,T,78,5.0       ,302,200.7",\
"17.53,98.374,349.8,1.4,1.2,2015-03-21, 0635,A,95,5.0       ,304.5,97.7",\
"17.528,98.362,329.1,1.4,1.2,2015-03-21, 0635,A,76,5.0       ,303.3,37.9",\
"18.252,103.121,367.1,1,1,2015-03-21, 0635,A,100,5.0       ,292.3,114",\
"18.251,103.112,362.1,1,1,2015-03-21, 0635,A,100,5.0       ,293.9,99.5",\
"17.465,98.027,317.5,1.5,1.2,2015-03-21, 0635,A,58,5.0       ,304.4,16.2",\
"17.534,98.368,355.2,1.4,1.2,2015-03-21, 0635,A,98,5.0       ,303.6,118",\
"17.544,98.366,322.9,1.4,1.2,2015-03-21, 0635,A,45,5.0       ,300.5,20.2",\
"17.542,98.353,331.4,1.4,1.2,2015-03-21, 0635,A,84,5.0       ,299.8,43.1",\
"17.54,98.34,355.5,1.4,1.2,2015-03-21, 0635,A,98,5.0       ,304.9,126.1",\
"17.551,98.339,338.7,1.4,1.2,2015-03-21, 0635,A,89,5.0       ,300.9,66.1",\
"18.101,101.418,314.1,1,1,2015-03-21, 0635,A,29,5.0       ,290.6,5.3",\
"17.623,98.346,359.2,1.4,1.2,2015-03-21, 0635,A,99,5.0       ,308.6,134.9",\
"17.621,98.333,324.4,1.4,1.2,2015-03-21, 0635,A,54,5.0       ,307.4,23.8",\
"17.24,96.154,322.2,2.1,1.4,2015-03-21, 0635,A,75,5.0       ,311.3,26.5",\
"18.125,101.453,326.6,1,1,2015-03-21, 0635,A,80,5.0       ,297.5,21.3",\
"17.62,98.196,313.9,1.5,1.2,2015-03-21, 0635,A,45,5.0       ,303.8,14.4",\
"17.617,98.181,323.8,1.5,1.2,2015-03-21, 0635,A,77,5.0       ,303.6,32.8",\
"18.148,101.488,365,1,1,2015-03-21, 0635,A,100,5.0       ,298,103.2",\
"18.147,101.479,350.1,1,1,2015-03-21, 0635,A,95,5.0       ,297.8,61.9",\
"17.628,98.177,373.9,1.5,1.2,2015-03-21, 0635,A,100,5.0       ,307.2,229.6",\
"18.157,101.487,321.4,1,1,2015-03-21, 0635,A,58,5.0       ,296.6,14.6",\
"18.25,102.058,342.2,1,1,2015-03-21, 0635,A,85,5.0       ,280.4,49.4",\
"18.166,101.485,320.3,1,1,2015-03-21, 0635,A,54,5.0       ,296.6,13.8",\
"17.485,97.126,311.2,1.7,1.3,2015-03-21, 0635,A,47,5.0       ,300.1,14.7",\
"17.896,99.581,322.5,1.2,1.1,2015-03-21, 0635,A,75,5.0       ,306.2,12.9",\
"17.617,97.847,315.8,1.5,1.2,2015-03-21, 0635,A,63,5.0       ,303.5,15.6",\
"17.492,97.119,313.2,1.7,1.3,2015-03-21, 0635,A,57,5.0       ,299.5,18.4",\
"18.201,101.415,323.2,1,1,2015-03-21, 0635,A,67,5.0       ,297.4,16.6",\
"17.729,98.361,328,1.4,1.2,2015-03-21, 0635,A,45,5.0       ,308.3,27.8",\
"17.633,97.797,316.2,1.6,1.2,2015-03-21, 0635,A,65,5.0       ,300.5,19.2",\
"17.631,97.783,320.9,1.6,1.2,2015-03-21, 0635,A,73,5.0       ,301.5,30.7",\
"17.732,98.254,335,1.4,1.2,2015-03-21, 0635,A,87,5.0       ,302.8,62.9",\
"17.73,98.242,347.8,1.4,1.2,2015-03-21, 0635,A,94,5.0       ,304.5,103.2",\
"18.236,101.4,401.5,1,1,2015-03-21, 0635,A,100,5.0       ,299.9,258.8",\
"17.743,98.252,353.9,1.4,1.2,2015-03-21, 0635,A,97,5.0       ,307.1,125.5",\
"17.741,98.239,331.1,1.4,1.2,2015-03-21, 0635,A,84,5.0       ,304.9,50",\
"17.766,98.26,320.9,1.4,1.2,2015-03-21, 0635,A,73,5.0       ,303.9,26.2",\
"17.764,98.248,314.4,1.4,1.2,2015-03-21, 0635,A,61,5.0       ,302.6,14.2",\
"17.299,95.533,323.1,2.3,1.5,2015-03-21, 0635,A,52,5.0       ,311.5,26.7",\
"18.26,101.377,361.8,1,1,2015-03-21, 0635,A,100,5.0       ,296.4,90.5",\
"18.259,101.367,345.4,1,1,2015-03-21, 0635,A,93,5.0       ,298.7,49.7",\
"17.74,98.038,331.9,1.5,1.2,2015-03-21, 0635,A,84,5.0       ,302.1,46.8",\
"18.189,100.835,321.5,1.1,1,2015-03-21, 0635,A,71,5.0       ,302.9,9.7",\
"18.132,100.457,330.6,1.1,1,2015-03-21, 0635,A,83,5.0       ,302.9,28.5",\
"17.753,98.051,355,1.5,1.2,2015-03-21, 0635,A,97,5.0       ,301.1,133.4",\
"17.751,98.036,360.8,1.5,1.2,2015-03-21, 0635,A,100,5.0       ,301.5,156",\
"17.748,98.021,325.6,1.5,1.2,2015-03-21, 0635,A,79,5.0       ,302.5,30.6",\
"18.387,102.11,342.2,1,1,2015-03-21, 0635,A,91,5.0       ,290.7,46.4",\
"18.286,101.424,335.5,1,1,2015-03-21, 0635,A,87,5.0       ,296.4,35.2",\
"18.285,101.415,324.1,1,1,2015-03-21, 0635,A,77,5.0       ,295.9,18.7",\
"18.198,100.837,327.8,1.1,1,2015-03-21, 0635,A,81,5.0       ,303.4,21.3",\
"18.14,100.459,322.4,1.1,1,2015-03-21, 0635,A,68,5.0       ,303.8,16.5",\
"17.92,99.085,324.3,1.3,1.1,2015-03-21, 0635,A,33,5.0       ,307.4,16.7",\
"17.749,98.06,339.1,1.5,1.2,2015-03-21, 0635,A,89,5.0       ,298.8,76.5",\
"17.746,98.045,358.5,1.5,1.2,2015-03-21, 0635,A,99,5.0       ,302.7,148.6",\
"17.744,98.03,324.1,1.5,1.2,2015-03-21, 0635,A,76,5.0       ,302.2,27.6",\
"18.33,101.659,324.1,1,1,2015-03-21, 0635,A,77,5.0       ,296.3,21.4",\
"18.164,100.558,321.5,1.1,1,2015-03-21, 0635,A,45,5.0       ,301.9,10.9",\
"18.163,100.548,324.3,1.1,1,2015-03-21, 0635,A,64,5.0       ,303.9,14.9",\
"17.792,98.25,316.2,1.4,1.2,2015-03-21, 0635,A,50,5.0       ,301,15.8",\
"17.757,98.043,345.1,1.5,1.2,2015-03-21, 0635,A,93,5.0       ,300.6,92.7",\
"18.089,100.013,320.5,1.1,1.1,2015-03-21, 0635,A,73,5.0       ,304.4,10.9",\
"17.803,98.249,377.9,1.4,1.2,2015-03-21, 0635,A,100,5.0       ,302.6,248",\
"17.8,98.235,340.3,1.4,1.2,2015-03-21, 0635,A,90,5.0       ,300.7,74.6",\
"17.768,98.041,332,1.5,1.2,2015-03-21, 0635,A,77,5.0       ,299.7,50.4",\
"18.432,102.237,319.6,1,1,2015-03-21, 0635,A,64,5.0       ,292.2,14.3",\
"17.82,98.286,341.6,1.4,1.2,2015-03-21, 0635,A,91,5.0       ,300.1,73.3",\
"17.817,98.273,420.2,1.4,1.2,2015-03-21, 0635,A,100,5.0       ,307.7,651.2",\
"17.815,98.26,361.2,1.4,1.2,2015-03-21, 0635,A,100,5.0       ,302.7,151.8",\
"18.333,101.494,322.4,1,1,2015-03-21, 0635,A,75,5.0       ,298.3,14.1",\
"18.332,101.485,328.2,1,1,2015-03-21, 0635,A,81,5.0       ,298.2,21.8",\
"18.216,100.713,324.6,1.1,1,2015-03-21, 0635,A,33,5.0       ,304.2,16.3",\
"17.838,98.334,318.7,1.4,1.2,2015-03-21, 0635,A,60,5.0       ,305,12.7",\
        ]

    strALine = ""
    for strALine in lstWeatherData:
        # we want the latest - so keep going until the end
        if len(strALine) > 0:
            fValue = getWindSpeed    (strALine)
            if fValue != None and fValue >= 0:
                fWindSpeed = fValue

            fValue = getWindDirection(strALine)
            if fValue != None and fValue > -361 and fValue <361:
                 fWindDirection = fValue


    # now check the fire data
    for strALine in lstFireData:
        # Where is the fire?
        if len(strALine) > 0:
            fFireLat       = getLatitude (strALine)
            fFireLong      = getLongitude(strALine)
            fFireMagnitude = getMagnitude(strALine)

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
