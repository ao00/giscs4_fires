# Conversion Functions

from getCSVStrFromIndex import *


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


#Test Function
def testGetCSVFloatFromIndex():
    strTestFireCSV = "2015-03-17 00:00:00,24.0,15.8,1014.8,SW,225,1.1,1.1,60,0.0,,,0.0,Cumulus v1.9.4,2015-03-16 17:00:00,"

    fvalue = getCSVFloatFromIndex(1, strTestFireCSV)
    if fvalue != 24.0:
        return False

    fvalue = getCSVFloatFromIndex(0, strTestFireCSV)
    if fvalue != None:
        return False

    fvalue = getCSVFloatFromIndex(100, strTestFireCSV)
    if fvalue != None:
        return False

    fvalue = getCSVFloatFromIndex(-1, strTestFireCSV)
    if fvalue != None:
        return False

    return True


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


#Test Get Fire Value Function
def testGetFireValueFunctions():
    strTestFireCSV = "-13.501,-172.57,311.5,3,1.6,2015-03-29, 0040,A,33,5.0       ,292.6,45.5"

    fValue = getLatitude(strTestFireCSV)
    if fValue != -13.501:
        return False

    fValue = getLongitude(strTestFireCSV)
    if fValue != -172.57:
        return False

    fValue = getMagnitude(strTestFireCSV)
    if fValue != 311.5:
        return False

    return True


#Wind Data
def getWindSpeed(zstrWeatherCSV):
    return getCSVFloatFromIndex(6, zstrWeatherCSV)


def getWindDirection(zstrWeatherCSV):
    return getCSVIntFromIndex(5, zstrWeatherCSV)


#Test Get Weather Value Function
def testGetWeatherValueFunctions():
    sTestCSV = "2015-03-17 00:00:00,24.0,15.8,1014.8,SW,225,1.1,1.1,60,0.0,,,0.0,Cumulus v1.9.4,2015-03-16 17:00:00,"

    fValue = getWindSpeed(sTestCSV)
    if fValue != 1.1:
        return False

    fValue = getWindDirection(sTestCSV)
    if fValue != 225:
        return False

    return True

