__author__ = 'adrianol'




import math
# http://www.sunearthtools.com/tools/distance.php Test Data

def getNewPositionFromDistanceAndDirection(zfLatStart, zfLongStart, zfBearing, zfDistanceInKM):
    fLatNew  = zfLatStart
    fLongNew = zfLongStart

    if zfDistanceInKM > 0:
        #var lat2 = Math.asin( Math.sin(lat1)*Math.cos(d/R) +
        #                     Math.cos(lat1)*Math.sin(d/R)*Math.cos(brng) );
        #var lon2 = lon1 + Math.atan2(Math.sin(brng)*Math.sin(d/R)*Math.cos(lat1),
        #                             Math.cos(d/R)-Math.sin(lat1)*Math.sin(lat2));

        fEarthRadiusInKM = 6371.0

        lat1  = math.radians(zfLatStart)
        long1 = math.radians(zfLongStart)

        brng = math.radians(zfBearing)

        fOverR = zfDistanceInKM / fEarthRadiusInKM

        lat2 = math.asin( math.sin(lat1) * math.cos(fOverR) +
                           math.cos(lat1) * math.sin(fOverR) * math.cos(brng) );

        fLatNew  = math.degrees(lat2)

        long2 = long1 + math.atan2(math.sin(brng) * math.sin(fOverR) * math.cos(lat1),
                                     math.cos(fOverR) - math.sin(lat1) * math.sin(lat2));

        fLongNew  = math.degrees(long2)


    return {'Latitude': fLatNew, 'Longitude': fLongNew}


def TestgetNewPositionFromDistanceAndDirection():
    Result = getNewPositionFromDistanceAndDirection(18.729000, 98.940700, 37, 1000)
    if round(Result['Latitude'], 2) != 25.81 and round(Result['Longitude'], 2) != 104.94:
        return False

    Result = getNewPositionFromDistanceAndDirection(18.729000, 98.940700, 136, 1000)
    if round(Result['Latitude'], 2) != 12.16 and round(Result['Longitude'], 2) != 105.32:
        return False

    Result = getNewPositionFromDistanceAndDirection(18.729000, 98.940700, 210, 1000)
    if round(Result['Latitude'], 2) != 10.89 and round(Result['Longitude'], 2) != 94.38:
        return False

    Result = getNewPositionFromDistanceAndDirection(18.729000, 98.940700, 310, 1000)
    if round(Result['Latitude'], 2) != 24.35 and round(Result['Longitude'], 2) != 91.39:
        return False

    return True