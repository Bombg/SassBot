import tanjun
import alluka
import hikari
import asyncio
import checkers.Chaturbate as Chaturbate
import checkers.Onlyfans as Onlyfans
import checkers.Fansly as Fansly
import checkers.Myfreecams as MFC
import checkers.Bongacams as BC
import checkers.Stripchat as SC
import checkers.Eplay as EP
from Constants import Constants
import checkers.Twitch as Twitch
import checkers.Kick as Kick
import checkers.Youtube as Youtube
import checkers.Cam4 as Cam4
import globals
import time
import StaticMethods
from Notifications import Notifications
from Database import Database
from typing import Callable
from datetime import date
import datetime
from datetime import timedelta

component = tanjun.Component()

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())

async def platformChecker(isOnlineFunc: Callable,platformNotifFunc: Callable, userName: str, platformName: str, rest: hikari.impl.RESTClientImpl):
    isOnline, title, thumbUrl, icon = await asyncio.get_running_loop().run_in_executor(None,isOnlineFunc,userName)
    isRerun = False
    db = Database()
    lastOnlineMessage,streamStartTime,streamEndTime = db.getPlatformAccountsRowValues(platformName,userName)
    tempTitle, tempTitleTime = db.getPlatformTempTitle(platformName, userName)
    secondsSinceTempTitle = StaticMethods.timeToSeconds(tempTitleTime)
    secondsSinceLastMessage = StaticMethods.timeToSeconds(lastOnlineMessage)
    secondsSinceStreamEndTime = StaticMethods.timeToSeconds(streamEndTime)
    secondsSinceStreamStartTime = StaticMethods.timeToSeconds(streamStartTime)
    if tempTitle and secondsSinceTempTitle < Constants.TEMP_TITLE_UPTIME:
        title = tempTitle
    if isOnline and StaticMethods.isRerun(title):
        isOnline = isOnline if db.getRerunAnnounce() else False
        isRerun = True
    if Constants.DEBUG:
        print(platformName + "Offline: " + str((-1 * secondsSinceStreamStartTime) if isOnline else secondsSinceStreamEndTime))
    if isOnline == True:
        db.setRerun(isRerun, platformName)
        if secondsSinceStreamEndTime >= Constants.WAIT_BETWEEN_MESSAGES and secondsSinceLastMessage >= Constants.WAIT_BETWEEN_MESSAGES and streamEndTime >= streamStartTime:
            print(f"{platformName}Boobies")
            await platformNotifFunc(rest, title, thumbUrl, icon, userName, isRerun)
            db.updatePlatformRowCol(platformName,"last_stream_start_time",time.time())
            db.updatePlatformAccountRowCol(platformName, userName,"last_stream_start_time",time.time())
            globals.rebroadcast[platformName] = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME or globals.rebroadcast[platformName]:
            print(f"Long{platformName}Boobies")
            await platformNotifFunc(rest, title, thumbUrl, icon, userName, isRerun)
            lastOnlineMessage = time.time()
            globals.rebroadcast[platformName] = 0
        elif streamEndTime >= streamStartTime:
            db.updatePlatformRowCol(platformName,"last_stream_start_time",time.time())
            db.updatePlatformAccountRowCol(platformName,userName,"last_stream_start_time",time.time())
    elif isOnline == False:
        db.setRerun(isRerun, platformName)
        if streamEndTime <= streamStartTime:
            db.updatePlatformRowCol(platformName,"last_stream_end_time",time.time())
            db.updatePlatformAccountRowCol(platformName,userName,"last_stream_end_time",time.time())
        globals.rebroadcast[platformName] = 0
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.CB_CHECK_TIMER)
async def checkChatur(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.cbUserName:
        for cbUserName in Constants.cbUserName:
            await platformChecker(Chaturbate.isModelOnline, Notifications.ChaturNotification,cbUserName,"chaturbate",rest)
            await asyncio.sleep(Constants.CB_CHECK_TIMER/len(Constants.cbUserName))

@component.with_schedule
@tanjun.as_interval(Constants.OF_CHECK_TIMER)
async def checkOnlyfans(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.ofUserName:
        for ofUserName in Constants.ofUserName:
            await platformChecker(Onlyfans.isModelOnline, Notifications.OFNotification,ofUserName,"onlyfans",rest)
            await asyncio.sleep(Constants.OF_CHECK_TIMER/len(Constants.ofUserName))

@component.with_schedule
@tanjun.as_interval(Constants.FANS_CHECK_TIMER)
async def checkFansly(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.fansUserName:
        for fansUserName in Constants.fansUserName:
            await platformChecker(Fansly.isModelOnline, Notifications.FansNotification,fansUserName,"fansly",rest)
            await asyncio.sleep(Constants.FANS_CHECK_TIMER/len(Constants.fansUserName))

@component.with_schedule
@tanjun.as_interval(Constants.TWITCH_CHECK_TIMER)
async def checkTwitch(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.twitchUserName:
        for twitchUserName in Constants.twitchUserName:
            await platformChecker(Twitch.isModelOnline, Notifications.TwitchNotification,twitchUserName,"twitch",rest)
            await asyncio.sleep(Constants.TWITCH_CHECK_TIMER/len(Constants.twitchUserName))

@component.with_schedule
@tanjun.as_interval(Constants.YT_CHECK_TIMER)
async def checkYT(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.ytUserName:
        for ytUserName in Constants.ytUserName:
            await platformChecker(Youtube.isModelOnline, Notifications.YTNotification,ytUserName,"youtube",rest)
            await asyncio.sleep(Constants.YT_CHECK_TIMER/len(Constants.ytUserName))

@component.with_schedule
@tanjun.as_interval(Constants.KICK_CHECK_TIMER)
async def checkKick(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.kickUserName:
        for kickUserName in Constants.kickUserName:
            await platformChecker(Kick.isModelOnline, Notifications.KickNotification,kickUserName,"kick",rest)
            await asyncio.sleep(Constants.KICK_CHECK_TIMER/len(Constants.kickUserName))

@component.with_schedule
@tanjun.as_interval(Constants.CAM4_CHECK_TIMER)
async def checkCam4(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.cam4UserName:
        for cam4UserName in Constants.cam4UserName:
            await platformChecker(Cam4.isModelOnline, Notifications.Cam4Notification,cam4UserName,"cam4",rest)
            await asyncio.sleep(Constants.CAM4_CHECK_TIMER/len(Constants.cam4UserName))

@component.with_schedule
@tanjun.as_interval(Constants.MFC_CHECK_TIMER)
async def checkMfc(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.mfcUserName:
        for mfcUserName in Constants.mfcUserName:
            await platformChecker(MFC.isModelOnline, Notifications.MfcNotification,mfcUserName,"mfc",rest)
            await asyncio.sleep(Constants.MFC_CHECK_TIMER/len(Constants.mfcUserName))


@component.with_schedule
@tanjun.as_interval(Constants.BC_CHECK_TIMER)
async def checkBc(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.bcUserName:
        for bcUserName in Constants.bcUserName:
            await platformChecker(BC.isModelOnline, Notifications.BcNotification,bcUserName,"bongacams",rest)
            await asyncio.sleep(Constants.BC_CHECK_TIMER/len(Constants.bcUserName))


@component.with_schedule
@tanjun.as_interval(Constants.SC_CHECK_TIMER)
async def checkSc(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.scUserName:
        for scUserName in Constants.scUserName:
            await platformChecker(SC.isModelOnline, Notifications.ScNotification,scUserName,"stripchat",rest)
            await asyncio.sleep(Constants.SC_CHECK_TIMER/len(Constants.scUserName))

@component.with_schedule
@tanjun.as_interval(Constants.EP_CHECK_TIMER)
async def checkEp(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.epUserName:
        for epUserName in Constants.epUserName:
            await platformChecker(EP.isModelOnline, Notifications.EpNotification,epUserName,"eplay",rest)
            await asyncio.sleep(Constants.EP_CHECK_TIMER/len(Constants.epUserName))


@component.with_schedule
@tanjun.as_interval(Constants.AVATAR_CHECK_TIMER)
async def changeAvatar(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    db = Database()
    online = StaticMethods.checkOnline(db)
    onTime, offTime, totalOnTime = db.getStreamTableValues()
    hours, minutes = StaticMethods.timeToHoursMinutes(offTime)
    if online and not globals.normalAvtar:
        await rest.edit_my_user(avatar = 'images/avatars/calmStreamer.png')
        print(f"changed avatar to good {Constants.streamerName}")
        globals.normalAvtar = True
    if not online and globals.normalAvtar and hours >= Constants.MIN_TIME_BEFORE_AVATAR_CHANGE and offTime != 0:
        await rest.edit_my_user(avatar = 'images/avatars/pissedStreamer.png')
        print(f"changed avatar to bad {Constants.streamerName}")
        globals.normalAvtar = False

@component.with_schedule
@tanjun.as_interval(Constants.STATUS_CHECK_TIMER)
async def changeStatus(bot: alluka.Injected[hikari.GatewayBot]) -> None:
    db = Database()
    subathon,subStart,subEnd = db.getSubathonStatusClean()
    playingString = StaticMethods.checkOnline(db)
    if subathon:
        hours, minutes = StaticMethods.timeToHoursMinutes(subStart)
        playingString = playingString + "athon H:" + str(hours) + "M:" +str(minutes) + " "
    if not playingString:
        playingString = playingString + "Offline "
    if playingString != globals.globalPlayString:
        print("Updated presence to " + playingString)
        globals.globalPlayString = playingString
        await asyncio.sleep(5)
        await bot.update_presence(activity=hikari.Activity(
            name = playingString, 
            type = hikari.ActivityType.STREAMING, 
            url = Constants.twitchUrl
            ))
        await asyncio.sleep(5)
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.STATUS_CHECK_TIMER)
async def checkOnlineTime() -> None:
    db = Database()
    online = StaticMethods.checkOnline(db)
    lastOnline,lastOffline,totalStreamTime = db.getStreamTableValues()
    if online and lastOffline >= lastOnline:
        print("time online starts now")
        db.setStreamLastOnline(time.time())
    elif not online and lastOffline <= lastOnline:
        print("offline time starts now")
        StaticMethods.setOfflineAddTime()
    print("\n")

@component.with_schedule
@tanjun.as_time_schedule(minutes=[5,15,25,35,45,55])
async def checkRestart() -> None:
    db = Database()
    onTime,offTime,totalTime = db.getStreamTableValues()
    online = StaticMethods.checkOnline(db)
    timeSinceRestart = time.time() - globals.botStartTime
    timeSinceOffline = time.time() - offTime
    if not online and timeSinceRestart > Constants.TIME_BEFORE_BOT_RESTART and timeSinceOffline > Constants.TIME_OFFLINE_BEFORE_RESTART:
        StaticMethods.safeRebootServer()
    elif Constants.DEBUG:
        print("TimeSinceRestart: " + str(timeSinceRestart))
        print("TimeSinceOffline: " + str(timeSinceOffline))

@component.with_schedule
@tanjun.as_time_schedule(minutes=[0,10,20,30,40,50])
async def presenceGrabber(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    members = rest.fetch_members(Constants.GUILD_ID)
    db = Database()
    online = StaticMethods.checkOnline(db)
    presencesDict = db.getPresenceDay(date.today())
    hourMinute = StaticMethods.getHourMinuteString()
    statusCounts = {}
    memberCount = 0
    if online:
        statusCounts["streaming"] = online
    async for member in members:
        memberCount += 1
        presence = member.get_presence()
        if presence != None:
            status = presence.visible_status
            statusStr = str(status)
            if statusStr in statusCounts:
                statusCounts[statusStr] += 1
            else:
                statusCounts[statusStr] = 1
    statusCounts["members"] = memberCount
    presencesDict[hourMinute] = statusCounts
    db.setPresenceDay(date.today(), presencesDict)

@component.with_schedule
@tanjun.as_time_schedule(minutes = [1,11,21,31,41,51])
async def smartAlert(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    db = Database()
    presencesDict = db.getPresenceDay(date.today())
    lastWeekPresenceDict = db.getLastWeeksDayPresenceData(date.today())
    hourMinute = StaticMethods.getHourMinuteString()
    lookAheadHourMinute = StaticMethods.getHourMinuteString(offset=Constants.SMART_ALERT_LOOK_AHEAD)
    if lastWeekPresenceDict:
        maxOnlineLastWeek = StaticMethods.getMaxOnlineInPresenceDict(lastWeekPresenceDict)
        if presencesDict[hourMinute] and lastWeekPresenceDict[lookAheadHourMinute]:
            lookAheadOnline = lastWeekPresenceDict[lookAheadHourMinute]['online']
            nowOnline = presencesDict[hourMinute]['online']
            onlineThreshold = int(maxOnlineLastWeek * Constants.PERCENTAGE_OF_MAX)
            if nowOnline >= onlineThreshold and lookAheadOnline >= onlineThreshold:
                StaticMethods.smartRebroadcast()

@component.with_schedule
@tanjun.as_interval(Constants.CONFESSION_CHECK_TIMER)
async def resetUnreviewedConfessions(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    StaticMethods.resetUnfinishedConfessions()
    db = Database()
    value = db.getAllUnreviewed()
    if value:
        minVal = 99
        minAlertsId = 0
        for val in value:
            if val[0] not in globals.confessionIds:
                globals.confessionIds[val[0]] = 1
            if minVal > globals.confessionIds[val[0]]:
                minVal = globals.confessionIds[val[0]]
                minAlertsId = val[0]
        alertIntervals = Constants.CONFESSION_ALERT_INTERVALS
        minVal = len(alertIntervals)-1 if minVal > len(alertIntervals)-1 else minVal
        if StaticMethods.timeToSeconds(globals.confessionIds["alert"]) >= alertIntervals[minVal]:
            globals.confessionIds[minAlertsId] += 1
            await rest.create_message(channel=Constants.CONFESSTION_CHANNEL_ID, content=f"There are {len(value)} confessions in need of review =)\n Use </confess-review:{Constants.CONFESS_REVIEW_COMMAND_ID}> to review them")
            globals.confessionIds["alert"] = time.time()
            for k, v in globals.confessionIds.items():
                if v < globals.confessionIds[minAlertsId]:
                    globals.confessionIds[k] = globals.confessionIds[minAlertsId]