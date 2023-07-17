import time
import os
from Database import Database
import globals
import base64
import datetime
from Constants import Constants
from datetime import timedelta
from datetime import date
import re

def isRerun(title:str) -> bool:
    reString = "(?i).*(^|!|\s|-|\()+((rerun|rr))(\s|-|\)|$)+.*"
    rerun = re.search(reString,title)
    return rerun

def replaceIntsWithString(minsDict: dict) -> dict:
    popKeys = []
    for k, v in minsDict.items():
        if minsDict[k] == 0:
            popKeys.append(k)
        else:
            minsDict[k] = minutesToHourMinString(minsDict[k])
    for key in popKeys:
        minsDict.pop(key)
    return minsDict

def minutesToHourMinString(minutes: int) -> str:
    hours = int(minutes / 60)
    mins = int(minutes % 60)
    return f"{hours}:{mins}"

def getWeekStreamingMinutes(startingDate: date, minutesDict = {}):
    db = Database()
    minutesBetweenOnlineChecks = 10
    daysInWeek = 7
    weekMinutes = {"CB":0,"OF":0,"Twitch":0,"YT":0,"Fans":0,"Kick":0,"TotalTimeStreaming":0} if not minutesDict else dict(minutesDict)
    platforms = list(weekMinutes)
    platforms.remove("TotalTimeStreaming")
    for i in range(daysInWeek):
        pastDate = startingDate - timedelta(days = i)
        dayData = db.getPresenceDay(pastDate)
        if dayData:
            for k, v in dayData.items():
                if v:
                    if 'streaming' in v.keys():
                        weekMinutes["TotalTimeStreaming"] += minutesBetweenOnlineChecks
                        if isinstance(v['streaming'],str):
                            for platform in platforms:
                                if platform in v['streaming']:
                                    weekMinutes[platform] += minutesBetweenOnlineChecks
                        else:
                            weekMinutes["Kick"] += minutesBetweenOnlineChecks
    return weekMinutes

def smartRebroadcast() -> None:
    platforms = ['chaturbate','onlyfans','fansly','twitch','youtube','kick']
    db = Database()
    for platform in platforms:
        lastOnlineMessage,streamStartTime,streamEndTime = db.getPlatformsRowValues(platform)
        secondsSinceLastMessage = timeToSeconds(lastOnlineMessage)
        if secondsSinceLastMessage >= Constants.SECONDS_BETWEEN_SMART_ALERTS and streamStartTime > streamEndTime:
            print(f"Smart alert for {platform}")
            globals.rebroadcast[platform] = 1

def getMaxOnlineInPresenceDict(presDict: dict) -> int:
    maxOnline = 0
    for k, v in presDict.items():
        if v:
            maxOnline = max(v["online"], maxOnline)
    return maxOnline


def getHourMinuteString(offset = 0):
    hour = datetime.datetime.now().hour
    hour += offset
    hour %= 24
    minute = datetime.datetime.now().minute
    minute = minute - (minute%10)
    hourMinute = f"{hour}:{minute}"
    return hourMinute

def get_file_content_chrome(driver, uri):
    result = driver.execute_async_script("""
    var uri = arguments[0];
    var callback = arguments[1];
    var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(){ callback(toBase64(xhr.response)) };
    xhr.onerror = function(){ callback(xhr.status) };
    xhr.open('GET', uri);
    xhr.send();
    """, uri)
    if type(result) == int :
        raise Exception("Request failed with status %s" % result)
    return base64.b64decode(result)

def setOfflineAddTime():
    db = Database()
    db.setStreamLastOffline(time.time())
    lastOnline,lastOffline,lastTotalStreamLength = db.getStreamTableValues()
    newTotalStreamLength = lastTotalStreamLength + (lastOffline -  lastOnline)
    db.setStreamLastStreamLength(newTotalStreamLength)

def getEmbedImage() -> str:
    db = Database()
    twImgList, twImgQue, bannedList = db.getTwImgStuff()
    url = checkImagePin()
    if not twImgQue and twImgList:
        twImgQue = twImgList
    if not twImgList:
        imageSrc = 'images/twitErrImg.jpg'
        print("adding default image for embed since nothing is on the list.")
    elif url:
        imageSrc = url
    else:
        imageSrc = twImgQue.pop(0)
        db.setTwImgQueue(twImgQue)
    return imageSrc

def unPin() -> None:
    db = Database()
    db.setImgPin(0, "")

def setRebroadcast() -> None:
    print("rebroadcast: On")
    globals.rebroadcast = {
        "chaturbate":1,
        "onlyfans":1,
        "fansly":1,
        "twitch":1,
        "youtube":1,
        "kick": 1
}

def addImageListQue(url: str) -> None:
    db = Database()
    twImgList, twImgQue,bannedList = db.getTwImgStuff()
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