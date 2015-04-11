__author__ = 'adrianol'

import time
import datetime
from getCSVStrFromIndex import *
from getCSVValueFromIndex import *
from getNewPosition import *
from getDistance import *
from getDirection import *

def getLatestAQDailyAverage(sAirQualityDailyAveragesLatest):
    # returns a dictionary of latest PM10 and/or PM2.5 AQI reading
    # we assume the file is in reverse order - i.e. look for first entry

    # Timestamp (GMT), PM10 (ug/m3), PM10AQI, PM2.5 (ug/m3), PM2.5AQI, CO, NO2, O3, SO2
    # 2015-04-11, 65.146, 56, 0, 0
    # 2015-04-10, 65.3124, 56, 0, 0

    try:
        fhData = open(sAirQualityDailyAveragesLatest)

        sALine = ""

        for sALine in fhData:
            # we want the latest - so keep going until the end
            if len(sALine) > 0:
                strTimeStamp = getCSVStrFromIndex  (0, sALine)
                fPM10        = getCSVFloatFromIndex(1, sALine)
                iPM10AQI     = getCSVIntFromIndex  (2, sALine)
                fPM25        = getCSVFloatFromIndex(3, sALine)
                iPM25AQI     = getCSVIntFromIndex  (4, sALine)

                if iPM10AQI != None and iPM25AQI != None:
                    try:
                        TimeStamp = time.mktime(time.strptime(strTimeStamp, '%Y-%m-%d'))

                        return [TimeStamp, iPM10AQI, iPM25AQI]

                    except:
                        # keep going...
                        TimeStamp = None

        return None

    except:
        return None

