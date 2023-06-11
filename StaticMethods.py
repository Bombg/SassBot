import time
import os
from Database import Database

def checkOnline(db: Database) -> str:
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

def timeToHoursMinutes(newTime: float) -> int:
    totalTime = time.time() - newTime
    totalTime = int(totalTime)
    totalTimeSeconds = int(totalTime % 60)
    totalTimeMinutes = int((totalTime - totalTimeSeconds) / 60)
    leftoverMinutes = totalTimeMinutes % 60
    totalTimeHours = int((totalTimeMinutes - leftoverMinutes ) / 60)
    return totalTimeHours, leftoverMinutes

def timeToHoursMinutesStartEnd(startTime: float, endTime: float) -> int:
    totalTime = endTime - startTime
    totalTime = int(totalTime)
    totalTimeSeconds = int(totalTime % 60)
    totalTimeMinutes = int((totalTime - totalTimeSeconds) / 60)
    leftoverMinutes = totalTimeMinutes % 60
    totalTimeHours = int((totalTimeMinutes - leftoverMinutes ) / 60)
    return totalTimeHours, leftoverMinutes

def timeToHoursMinutesTotalTime(totalTime: float) -> int:
    totalTime = int(totalTime)
    totalTimeSeconds = int(totalTime % 60)
    totalTimeMinutes = int((totalTime - totalTimeSeconds) / 60)
    leftoverMinutes = totalTimeMinutes % 60
    totalTimeHours = int((totalTimeMinutes - leftoverMinutes ) / 60)
    return totalTimeHours, leftoverMinutes

def timeToSeconds(newTime: float) -> int:
    totalTime = time.time() - newTime
    totalTime = int(totalTime)
    return totalTime

def rebootServer() -> None:
    os.system('reboot')

def safeRebootServer() -> None:
    time.sleep(300)
    print("Scheduled restart is happening.\nSleeping for 300 seconds before restart, in case something goes horribly wrong")
    rebootServer()