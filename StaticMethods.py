import time
import os
from Database import Database
import asyncio
from Constants import Constants
import globals

def unPin() -> None:
    db = Database()
    db.setImgPin(0, "")

async def setRebroadcast() -> None:
    globals.rebroadcast = True
    print("rebroadcast: On")
    await asyncio.sleep(Constants.onlineCheckTimer + 20)
    globals.rebroadcast = False
    print("rebroadcast: Off")

def addImageListQue(url: str) -> None:
    db = Database()
    twImgList, twImgQue = db.getTwImgStuff()
    twImgList.insert(0, url)
    db.setTwImgList(twImgList)
    twImgQue.insert(0,url)
    db.setTwImgQueue(twImgQue)

def pinImage(url: str, hours: int) -> None:
    currentTime = time.time()
    addedSeconds = hours * 60 * 60
    pinEndEpochTime = currentTime + addedSeconds
    db = Database()
    db.setImgPin(pinEndEpochTime, url)

def checkImagePin():
    url = ""
    db = Database()
    pinTime, pinUrl = db.getImgPin()
    if pinTime is None:
        pinTime = 0
    if time.time() < pinTime:
        url = pinUrl
    return url

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