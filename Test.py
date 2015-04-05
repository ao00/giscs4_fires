# Conversion Functions

from getCSVValueFromIndex import *
from getCSVStrFromIndex import *
from getDirection import *
from getDistance import *
from getNewPosition import *

#Master Test Function
def masterTestFunction():

    if not testGetCSVStrFromIndex():
        return False

    if not testGetCSVFloatFromIndex():
        return False

    if not testGetFireValueFunctions():
        return False

    if not testGetWeatherValueFunctions():
        return False

    if not TestgetDirection():
        return False

    if not TestgetDistance():
        return False

    if not TestgetNewPositionFromDistanceAndDirection():
        return False

    return True


#testMode = False
testMode = True
if testMode:
    if not masterTestFunction():
        print "Regression Test Failed"
        
