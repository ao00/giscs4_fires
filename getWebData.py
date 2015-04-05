
import time
import datetime
import urllib3

def getLatestWeatherData(sWeatherDataFilename):
    try:

        # http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ICHANGWA3&day=1&month=3&year=2015&dayend=1&monthend=4&yearend=2015&graphspan=custom&format=1

#        sURLRequest = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ICHIANGM6&day=" + time.strftime("%d") +\
#                      "&month=" + time.strftime("%m") +\
#                     "&year=" + time.strftime("%Y") +\
#                      "&graphspan=day&format=1"

        datafile = open(sWeatherDataFilename, "wt")

        tmTimeStamp = time.time() - 24 * 60 * 60
        dtYesterday = datetime.datetime.fromtimestamp(tmTimeStamp)
        # yesterday's weather...
        sURLRequest = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ICHANGWA3&day=" + dtYesterday.strftime("%d") +\
                      "&month=" + dtYesterday.strftime("%m") +\
                     "&year=" + dtYesterday.strftime("%Y") +\
                      "&graphspan=day&format=1"

        http = urllib3.PoolManager()
        request = http.request('GET', sURLRequest)

        responseCode = request.status
        if responseCode == 200:
            # save the content to file
            try:
                datafile.write(request.data)

            except:
                print "failed to save data"

        # today's weather...
        sURLRequest = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ICHANGWA3&day=" + time.strftime("%d") +\
                      "&month=" + time.strftime("%m") +\
                     "&year=" + time.strftime("%Y") +\
                      "&graphspan=day&format=1"

        http = urllib3.PoolManager()
        request = http.request('GET', sURLRequest)

        responseCode = request.status
        if responseCode == 200:
            # save the content to file
            try:
                datafile.write(request.data)

            except:
                print "failed to save data"

        datafile.close()
        return True

    except:
        print "failed to get data"

    return False


def getLatestFireData(sFireDataFilename):
    try:

        #sURLRequest = "http://pw.ajosoft.com/pwseasiafires24h.php"
        #sURLRequest = "http://pw.ajosoft.com/pwsasiafires24h.php"
        sURLRequest = "http://pw.ajosoft.com/pwglobalfires48h.php"


        http = urllib3.PoolManager(timeout=30.0)
        request = http.request('GET', sURLRequest)

        responseCode = request.status
        if responseCode == 200:
            # save the content to file
            try:
                datafile = open(sFireDataFilename, "wt")
                datafile.write(request.data)
                datafile.close()

                return True


            except:
                print "failed to save data"
    except urllib3.exceptions.SSLError as e:
        print e

    except:
        print "failed to get data"

    return False

def getLatestWebData(sFireDataFilename, sWeatherDataFilename):
    getLatestWeatherData(sWeatherDataFilename)
    getLatestFireData(sFireDataFilename)

    
