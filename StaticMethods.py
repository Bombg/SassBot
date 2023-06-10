import time
import os
import Database


@staticmethod
def checkOnline(db):
    playingString = ""
    cbLastOnlineMessage,cbStreamStartTime,cbStreamEndTime = db.getPlatformsRowValues('chaturbate')
    ofLastOnlineMessage,ofStreamStartTime,ofStreamEndTime = db.getPlatformsRowValues('onlyfans')
    twitchLastOnlineMessage,twitchStreamStartTime,twitchStreamEndTime = db.getPlatformsRowValues('twitch')
    ytLastOnlineMessage,ytStreamStartTime,ytStreamEndTime = db.getPlatformsRowValues('youtube')
    fansLastOnlineMessage,fansStreamStartTime,fansStreamEndTime = db.getPlatformsRowValues('fansly')
    kickLastOnlineMessage,kickStreamStartTime,kickStreamEndTime = db.getPlatformsRowValues('kick')
    if cbStreamStartTime > cbStreamEndTime:
        playingString = playingString + "CB "
    if ofStreamStartTime > ofStreamEndTime:
        playingString = playingString + "OF "
    if twitchStreamStartTime > twitchStreamEndTime:
        playingString = playingString + "Twitch "
    if ytStreamStartTime > ytStreamEndTime:
        playingString = playingString + "YT "
    if fansStreamStartTime > fansStreamEndTime:
        playingString = playingString + "Fans "
    if kickStreamStartTime > kickStreamEndTime:
        playingString = playingString + "Kick"
    return playingString

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
def timeToHoursMinutesStartEnd(startTime, endTime):
    totalTime = endTime - startTime
    totalTime = int(totalTime)
    totalTimeSeconds = int(totalTime % 60)
    totalTimeMinutes = int((totalTime - totalTimeSeconds) / 60)
    leftoverMinutes = totalTimeMinutes % 60
    totalTimeHours = int((totalTimeMinutes - leftoverMinutes ) / 60)

    return totalTimeHours, leftoverMinutes

@staticmethod
def timeToHoursMinutesTotalTime(totalTime):
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

@staticmethod
def rebootServer():
    os.system('reboot')

@staticmethod
def safeRebootServer():
    time.sleep(300)
    print("Scheduled restart is happening.\nSleeping for 300 seconds before restart, in case something goes horribly wrong")
    rebootServer()