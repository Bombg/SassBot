import time
import os
from utils.Database import Database
import globals
import datetime
from DefaultConstants import Settings as Settings
from datetime import timedelta
from datetime import date
import re
import tanjun
import logging
import secrets
import hashlib
import base64
from urllib.parse import urlencode, urlunparse, urlparse
import hikari

baseSettings = Settings()
logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

def logCommand(funcName, ctx) -> None:
    file = open("commandLogs.txt", 'a')
    date = datetime.datetime.fromtimestamp(time.time())
    if isinstance(ctx, tanjun.abc.SlashContext):
        file.write(f"{date} - {funcName} - used by {ctx.member.id} aka {ctx.member.display_name}\n")
    else:
        logger.warning("didn't get right ctx for command logger")
    file.close()

def resetUnfinishedConfessions():
    db = Database()
    unFinished = db.getUnfinishedConfessionReviews()
    if unFinished:
        for row in unFinished:
            if timeToSeconds(row[1]) >= baseSettings.TIME_BEFORE_REVIEW_RESET:
                db.resetConfessionDateReviewed(row[0])

def resetUnfinishedAppeals():
    db = Database()
    unFinished = db.getUnfinishedAppealReviews()
    if unFinished:
        for row in unFinished:
            if timeToSeconds(row[1]) >= baseSettings.TIME_BEFORE_REVIEW_RESET:
                db.resetAppealDateReviewed(row[0])

async def isPermission(ctx: tanjun.abc.SlashContext)-> bool:
    hasPermission = False
    roles = ctx.member.get_roles()
    #canBan = ctx.member.permissions & hikari.Permissions.BAN_MEMBERS
    if not baseSettings.whiteListedRoleIDs:
        logger.warning("No one in whiteListedRoleIDs, no one can use mod commands")
    for role in roles:
        if role.id in baseSettings.whiteListedRoleIDs or ctx.member.id in baseSettings.whiteListedRoleIDs:
            hasPermission = True
    if not hasPermission:
        ctx.set_ephemeral_default(True)
        await ctx.respond("You don't have permission to do this")
    return hasPermission

def isRerun(title:str) -> bool:
    reString = "(?i).*([^a-zA-Z]|^)+((rerun|rr|𝓡𝓡|𝓡𝓔𝓡𝓤𝓝|not live))([^a-zA-Z]|$)+.*"
    rerun = re.search(reString,title)
    return rerun

def replaceIntsWithString(minsDict: dict) -> dict:
    popKeys = []
    minsDict = minsDict.copy()
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
    weekMinutes = {"CB":0,"OF":0,"Twitch":0,"YT":0,"Fans":0,"Kick":0,"Cam4":0, "MFC":0, "BC":0 , "SC":0,"EP":0,"MV":0,"TotalTimeStreamingLive":0, "TotalTimeStreamingReruns":0} if not minutesDict else dict(minutesDict)
    platforms = list(weekMinutes)
    platforms.remove("TotalTimeStreamingLive")
    platforms.remove("TotalTimeStreamingReruns")
    for i in range(daysInWeek):
        pastDate = startingDate - timedelta(days = i)
        dayData = db.getPresenceDay(pastDate)
        if dayData:
            for k, v in dayData.items():
                if v:
                    if 'streaming' in v.keys():
                        notOnlyRerunsFlag = False
                        if isinstance(v['streaming'],str):
                            if "RR" in v['streaming']:
                                weekMinutes["TotalTimeStreamingReruns"] += minutesBetweenOnlineChecks
                            for platform in platforms:
                                if platform in v['streaming'] and not "RR-" + platform in v['streaming']:
                                    weekMinutes[platform] += minutesBetweenOnlineChecks
                                    notOnlyRerunsFlag = True
                        if notOnlyRerunsFlag:
                            weekMinutes["TotalTimeStreamingLive"] += minutesBetweenOnlineChecks
    return weekMinutes

def smartRebroadcast() -> None:
    db = Database()
    platforms = db.GetPlatformNames()
    for platform in platforms:
        lastOnlineMessage,streamStartTime,streamEndTime,isRerun = db.getPlatformsRowValues(platform)
        secondsSinceLastMessage = timeToSeconds(lastOnlineMessage)
        if secondsSinceLastMessage >= baseSettings.SECONDS_BETWEEN_SMART_ALERTS and streamStartTime > streamEndTime:
            logger.info(f"Smart alert for {platform}")
            globals.rebroadcast[platform] = 1

def getMaxOnlineInPresenceDict(presDict: dict) -> int:
    maxOnline = 0
    for k, v in presDict.items():
        if v and 'online' in v:
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
        imageSrc = baseSettings.defaultThumbnail
        logger.info("adding default image for embed since nothing is on the image list.")
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
    logger.info("rebroadcast: On")
    db = Database()
    platforms = db.GetPlatformNames()
    for platform in platforms:
        globals.rebroadcast[platform] = 1

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
    cbLastOnlineMessage,cbStreamStartTime,cbStreamEndTime, cbIsRerun = db.getPlatformsRowValues('chaturbate')
    ofLastOnlineMessage,ofStreamStartTime,ofStreamEndTime, ofIsRerun = db.getPlatformsRowValues('onlyfans')
    twitchLastOnlineMessage,twitchStreamStartTime,twitchStreamEndTime, twitchIsRerun = db.getPlatformsRowValues('twitch')
    ytLastOnlineMessage,ytStreamStartTime,ytStreamEndTime, ytIsRerun = db.getPlatformsRowValues('youtube')
    fansLastOnlineMessage,fansStreamStartTime,fansStreamEndTime, fansIsRerun = db.getPlatformsRowValues('fansly')
    kickLastOnlineMessage,kickStreamStartTime,kickStreamEndTime, kickIsRerun = db.getPlatformsRowValues('kick')
    cam4LastOnlineMessage,cam4StreamStartTime,cam4StreamEndTime, cam4IsRerun = db.getPlatformsRowValues('cam4')
    mfcLastOnlineMessage,mfcStreamStartTime,mfcStreamEndTime, mfcIsRerun = db.getPlatformsRowValues('mfc')
    bcLastOnlineMessage,bcStreamStartTime,bcStreamEndTime, bcIsRerun = db.getPlatformsRowValues('bongacams')
    scLastOnlineMessage,scStreamStartTime,scStreamEndTime, scIsRerun = db.getPlatformsRowValues('stripchat')
    epLastOnlineMessage,epStreamStartTime,epStreamEndTime, epIsRerun = db.getPlatformsRowValues('eplay')
    mvLastOnlineMessage,mvStreamStartTime,mvStreamEndTime, mvIsRerun = db.getPlatformsRowValues('manyvids')
    if cbStreamStartTime > cbStreamEndTime:
        playingString = playingString + "RR-CB " if cbIsRerun else playingString + "CB "
    if ofStreamStartTime > ofStreamEndTime:
        playingString = playingString + "RR-OF " if ofIsRerun else playingString + "OF "
    if twitchStreamStartTime > twitchStreamEndTime:
        playingString = playingString + "RR-Twitch " if twitchIsRerun else playingString + "Twitch "
    if ytStreamStartTime > ytStreamEndTime:
        playingString = playingString + "RR-YT " if ytIsRerun else playingString + "YT "
    if fansStreamStartTime > fansStreamEndTime:
        playingString = playingString + "RR-Fans " if fansIsRerun else playingString + "Fans "
    if kickStreamStartTime > kickStreamEndTime:
        playingString = playingString + "RR-Kick " if kickIsRerun else playingString + "Kick "
    if cam4StreamStartTime > cam4StreamEndTime:
        playingString = playingString + "RR-Cam4 " if cam4IsRerun else playingString + "Cam4 "
    if mfcStreamStartTime > mfcStreamEndTime:
        playingString = playingString + "RR-MFC " if mfcIsRerun else playingString + "MFC "
    if bcStreamStartTime > bcStreamEndTime:
        playingString = playingString + "RR-BC " if bcIsRerun else playingString + "BC "
    if scStreamStartTime > scStreamEndTime:
        playingString = playingString + "RR-SC " if scIsRerun else playingString + "SC "
    if epStreamStartTime > epStreamEndTime:
        playingString = playingString + "RR-EP " if epIsRerun else playingString + "EP "
    if mvStreamStartTime > mvStreamEndTime:
        playingString = playingString + "RR-MV " if mvIsRerun else playingString + "MV "
    if playingString and playingString[-1] == " ":
        playingString = playingString[:-1]
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
    if newTime == None:
        newTime = 0
    totalTime = time.time() - newTime
    totalTime = int(totalTime)
    return totalTime

def rebootServer() -> None:
    logger.critical("Sassbot server rebooting from restart command or fd leak detection or scheduled restart based off TIME_BEFORE_BOT_RESTART")
    globals.botStartTime = time.time()
    os.system('reboot')

def safeRebootServer() -> None:
    logger.warning("Scheduled restart is happening.\nSleeping for 300 seconds before restart, in case something goes horribly wrong")
    time.sleep(300)
    rebootServer()

def GetThumbnail(tempThumbUrl, constantsThumbnail):
    thumbnail = ""
    if constantsThumbnail == "LIST":
        thumbnail = ""
    elif constantsThumbnail:
        thumbnail = constantsThumbnail
    elif tempThumbUrl:
        thumbnail = tempThumbUrl
    
    return thumbnail

def GetProxies(proxyIpPort):
    proxies = {
    'http': f'socks5://{proxyIpPort}',
    'https': f'socks5://{proxyIpPort}'
    }
    return proxies

def GetShortestActiveCheckTimer():
    timerLengths = []
    noDriverTimerLengths = []
    if baseSettings.kickUserName and baseSettings.kickClientId:
        timerLengths.append(baseSettings.KICK_CHECK_TIMER)
    else:
        noDriverTimerLengths.append(baseSettings.KICK_CHECK_TIMER)
    if baseSettings.cbUserName:
        timerLengths.append(baseSettings.CB_CHECK_TIMER)
    if baseSettings.fansUserName:
        noDriverTimerLengths.append(baseSettings.FANS_CHECK_TIMER)
    if baseSettings.ofUserName:
        noDriverTimerLengths.append(baseSettings.OF_CHECK_TIMER)
    if baseSettings.ytUserName:
        timerLengths.append(baseSettings.YT_CHECK_TIMER)
    if baseSettings.twitchUserName:
        timerLengths.append(baseSettings.TWITCH_CHECK_TIMER)
    if baseSettings.cam4UserName:
        timerLengths.append(baseSettings.CAM4_CHECK_TIMER)
    if baseSettings.mfcUserName:
        timerLengths.append(baseSettings.MFC_CHECK_TIMER)
    if baseSettings.bcUserName:
        timerLengths.append(baseSettings.BC_CHECK_TIMER)
    if baseSettings.scUserName:
        timerLengths.append(baseSettings.SC_CHECK_TIMER)
    if baseSettings.epUserName:
        timerLengths.append(baseSettings.EP_CHECK_TIMER)
    if baseSettings.mvUserName:
        timerLengths.append(baseSettings.MV_CHECK_TIMER)
    shortest = 999999999999999999
    ndShortest = 999999999999999999
    for timer in timerLengths:
        if timer < shortest:
            shortest = timer
    for timer in noDriverTimerLengths:
        if timer < ndShortest:
            ndShortest = timer
    return shortest, ndShortest

class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/health"

def GetCodeVerifier():
    codeVerifier = secrets.token_urlsafe(64)
    return codeVerifier

def GetOauthState():
    return secrets.token_urlsafe(32)

def GetHashedCodeVerifier(codeVerifier):
    return hashlib.sha256(codeVerifier.encode('utf-8')).digest()

def GetCodeChallenge(hashedVerifier):
    return base64.urlsafe_b64encode(hashedVerifier).rstrip(b'=').decode('utf-8')

def EncodeParamsWithUrl(params: dict, url:str) -> str:
    encoded_params = urlencode(params)
    parsedUrl = urlparse(url)
    fullUrl = urlunparse(parsedUrl._replace(query=encoded_params))
    return fullUrl

def GetKickClipUrlFromClipId(clipId:str) -> str:
    clipUrl = ""
    if clipId:
        db = Database()
        slug = db.GetChannelSlugFromClipId(clipId)
        clipUrl = f'https://kick.com/{slug}/clips/{clipId}'
    return clipUrl
