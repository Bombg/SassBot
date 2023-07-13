import tanjun
import alluka
import hikari
import asyncio
import checkers.Chaturbate as Chaturbate
import checkers.Onlyfans as Onlyfans
import checkers.Fansly as Fansly
from Constants import Constants
import checkers.Twitch as Twitch
import checkers.Kick as Kick
import checkers.Youtube as Youtube
import globals
import time
import StaticMethods
from Notifications import Notifications
from Database import Database
from typing import Callable
from datetime import date
import datetime

component = tanjun.Component()

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())

async def platformChecker(isOnlineFunc: Callable,platformNotifFunc: Callable, urlConstant: str, platformName: str, rest: hikari.impl.RESTClientImpl):
    isOnline, title, thumbUrl, icon = await asyncio.get_running_loop().run_in_executor(None,isOnlineFunc,urlConstant)
    db = Database()
    lastOnlineMessage,streamStartTime,streamEndTime = db.getPlatformsRowValues(platformName)
    secondsSinceLastMessage = StaticMethods.timeToSeconds(lastOnlineMessage)
    secondsSinceStreamEndTime = StaticMethods.timeToSeconds(streamEndTime)
    secondsSinceStreamStartTime = StaticMethods.timeToSeconds(streamStartTime)
    if Constants.DEBUG:
        print(platformName + "Offline: " + str((-1 * secondsSinceStreamStartTime) if isOnline else secondsSinceStreamEndTime))
    if isOnline == 3:
        print(f"{platformName} check failed cause bot detection")
    elif isOnline == True:
        if secondsSinceStreamEndTime >= Constants.WAIT_BETWEEN_MESSAGES and secondsSinceLastMessage >= Constants.WAIT_BETWEEN_MESSAGES and streamEndTime >= streamStartTime:
            print(f"{platformName}Boobies")
            await platformNotifFunc(rest, title, thumbUrl, icon)
            db.updateTableRowCol("platforms",platformName,"last_stream_start_time",time.time())
            globals.rebroadcast[platformName] = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME or globals.rebroadcast[platformName]:
            print(f"Long{platformName}Boobies")
            await platformNotifFunc(rest, title, thumbUrl, icon)
            lastOnlineMessage = time.time()
            globals.rebroadcast[platformName] = 0
        elif streamEndTime > streamStartTime:
            db.updateTableRowCol("platforms",platformName,"last_stream_start_time",time.time())
    elif isOnline == False:
        if streamEndTime <= streamStartTime:
            db.updateTableRowCol("platforms",platformName,"last_stream_end_time",time.time())
        globals.rebroadcast[platformName] = 0
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.ONLINE_CHECK_TIMER)
async def checkChatur(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.cbApiUrl:
        await platformChecker(Chaturbate.isModelOnline, Notifications.ChaturNotification,Constants.cbApiUrl,"chaturbate",rest)

@component.with_schedule
@tanjun.as_interval(Constants.ONLINE_CHECK_TIMER)
async def checkOnlyfans(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.ofUrl:
        await platformChecker(Onlyfans.isModelOnline, Notifications.OFNotification,Constants.ofUrl,"onlyfans",rest)

@component.with_schedule
@tanjun.as_interval(Constants.ONLINE_CHECK_TIMER)
async def checkFansly(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.fansUrl:
        await platformChecker(Fansly.isModelOnline, Notifications.FansNotification,Constants.fansUrl,"fansly",rest)

@component.with_schedule
@tanjun.as_interval(Constants.ONLINE_CHECK_TIMER)
async def checkTwitch(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.twitchChannelName:
        await platformChecker(Twitch.isModelOnline, Notifications.TwitchNotification,Constants.twitchChannelName,"twitch",rest)

@component.with_schedule
@tanjun.as_interval(Constants.ONLINE_CHECK_TIMER)
async def checkYT(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.ytUrl:
        await platformChecker(Youtube.isModelOnline, Notifications.YTNotification,Constants.ytUrl,"youtube",rest)

@component.with_schedule
@tanjun.as_interval(Constants.ONLINE_CHECK_TIMER)
async def checkKick(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.kickUrl:
        await platformChecker(Kick.isModelOnline, Notifications.KickNotification,Constants.kickUserName,"kick",rest)

@component.with_schedule
@tanjun.as_interval(Constants.LONG_ONLINE_CHECK_TIMER)
async def checkKittiesKick(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if Constants.kittiesKickUrl:
        await platformChecker(Kick.isModelOnline, Notifications.KittiesKickNotification,Constants.kittiesKickUserName,"kittiesKick",rest)

@component.with_schedule
@tanjun.as_interval(Constants.AVATAR_CHECK_TIMER)
async def changeAvatar(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    db = Database()
    online = StaticMethods.checkOnline(db)
    onTime, offTime, totalOnTime = db.getStreamTableValues()
    hours, minutes = StaticMethods.timeToHoursMinutes(offTime)
    if online and not globals.normalAvtar:
        await rest.edit_my_user(avatar = 'images/avatars/calmCass.png')
        print(f"changed avatar to good {Constants.streamerName}")
        globals.normalAvtar = True
    if not online and globals.normalAvtar and hours >= Constants.MIN_TIME_BEFORE_AVATAR_CHANGE and offTime != 0:
        await rest.edit_my_user(avatar = 'images/avatars/missCass.png')
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
            url = "https://www.twitch.tv/kitty_cass_"
            ))
        await asyncio.sleep(5)
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.STATUS_CHECK_TIMER)
async def checkOnlineTime() -> None:
    db = Database()
    online = StaticMethods.checkOnline(db)
    lastOnline,lastOffline,totalStreamTime = db.getStreamTableValues()
    if online:
        online = True
    else:
        online = False
    if online and lastOffline > lastOnline:
        print("time online starts now")
        db.setStreamLastOnline(time.time())
    elif not online and lastOffline < lastOnline:
        print("offline time starts now")
        StaticMethods.setOfflineAddTime()
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.RESTART_CHECK_TIMER)
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
        