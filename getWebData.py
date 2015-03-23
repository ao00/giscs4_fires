
import time
import urllib3

def getLatestWeatherData():
    try:

        sURLRequest = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ICHIANGM6&day=" + time.strftime("%d") +\
                      "&month=" + time.strftime("%m") +\
                     "&year=" + time.strftime("%Y") +\
                      "&graphspan=day&format=1"


        http = urllib3.PoolManager()
        request = http.request('GET', sURLRequest)

        responseCode = request.status
        if responseCode == 200:
            # save the content to file
            try:
                datafile = open("WeatherData.csv", "wt")
                datafile.write(request.data)
                datafile.close()

                return True


            except:
                print "failed to save data"

    except:
        print "failed to get data"

    return False


def getLatestFireData():
    try:

        #sURLRequest = "http://pw.ajosoft.com/pwseasiafires24h.php"
        #sURLRequest = "http://pw.ajosoft.com/pwsasiafires24h.php"
        sURLRequest = "http://pw.ajosoft.com/pwglobalfires24h.php"


        http = urllib3.PoolManager(timeout=30.0)
        request = http.request('GET', sURLRequest)

        responseCode = request.status
        if responseCode == 200:
            # save the content to file
            try:
                datafile = open("FireData.csv", "wt")
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

def getLatestWebData():
    getLatestFireData()
    getLatestWeatherData()
    
    
