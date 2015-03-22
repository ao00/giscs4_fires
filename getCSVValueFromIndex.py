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


#Fire Data
def getLatitude(zstrFireCSV):
    return getCSVFloatFromIndex(1, zstrFireCSV)


def getLongitude(zstrFireCSV):
    return getCSVFloatFromIndex(2, zstrFireCSV)


def getMagnitude(zstrFireCSV):
    return getCSVFloatFromIndex(3, zstrFireCSV)


#Test Get Fire Value Function
def testGetFireValueFunctions():
    strTestFireCSV = "2015-03-17 00:00:00,24.0,15.8,1014.8,SW,225,1.1,1.1,60,0.0,,,0.0,Cumulus v1.9.4,2015-03-16 17:00:00,"

    fValue = getLatitude(strTestFireCSV)
    if fValue != 24.0:
        return False

    fValue = getLongitude(strTestFireCSV)
    if fValue != 15.8:
        return False

    fValue = getMagnitude(strTestFireCSV)
    if fValue != 1014.8:
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

