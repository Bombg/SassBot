import time
import globals


@staticmethod
def checkOnline():
    online = False
    if globals.chaturFalse <= 0:
        online = True
    elif globals.onlyFalse <= 0:
        online = True
    elif globals.twitchFalse <= 0:
        online = True
    elif globals.ytFalse <= 0:
        online = True
    elif globals.fansFalse <= 0:
        online = True
    elif globals.kickFalse <= 0:
        online = True
    else:
        online = False
    return online

@staticmethod
def timeToHoursMinutes(newTime):
    totalTime = time.time() - newTime
    totalTime = int(totalTime)
    totalTimeSeconds = int(totalTime % 60)
    totalTimeMinutes = int((totalTime - totalTimeSeconds) / 60)
    leftoverMinutes = totalTimeMinutes % 60
    totalTimeHours = int((totalTimeMinutes - leftoverMinutes ) / 60)

    return totalTimeHours, leftoverMinutes

@staticmethod
def timeToSeconds(newTime):
    totalTime = time.time() - newTime
    totalTime = int(totalTime)
    return totalTime