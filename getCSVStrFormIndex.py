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


# Test Function
def testGetCSVStrFromIndex():
    sTestCSV = "2015-03-17 00:00:00,24.0,15.8,1014.8,SW,225,1.1,1.1,60,0.0,,,0.0,Cumulus v1.9.4,2015-03-16 17:00:00,"

    strResults = getCSVStrFromIndex(0, sTestCSV)
    if strResults != "2015-03-17 00:00:00":
        return False

    strResults = getCSVStrFromIndex(2, sTestCSV)
    if strResults != "15.8":
        return False

    strResults = getCSVStrFromIndex(100, sTestCSV)
    if strResults != "":
        return False

    strResults = getCSVStrFromIndex(-1, sTestCSV)
    if strResults != "":
        return False

    strResults = getCSVStrFromIndex(0, "")
    if strResults != "":
        return False

    return True
    
