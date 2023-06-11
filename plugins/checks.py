import tanjun
import alluka
import hikari
import asyncio
import checkers.ChaturCas as ChaturCas
import checkers.OnlyCas as OnlyCas
import checkers.FansCas as FansCas
from Constants import Constants
import checkers.TwitchCas as TwitchCas
import checkers.KickCass as KickCass
import checkers.YouCas as YouCas
import globals
import time
import StaticMethods
from Notifications import Notifications
from Database import Database
from typing import Callable

component = tanjun.Component()

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())

async def platformChecker(isOnlineFunc: Callable,platformNotifFunc: Callable, urlConstant: str, platformName: str, rest: hikari.impl.RESTClientImpl):
    isOnline, title = await asyncio.get_running_loop().run_in_executor(None,isOnlineFunc,urlConstant)
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
            await platformNotifFunc(rest, title)
            db.updateTableRowCol("platforms",platformName,"last_stream_start_time",time.time())
            globals.rebroadcast[platformName] = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME or globals.rebroadcast[platformName]:
            print(f"Long{platformName}Boobies")
            await platformNotifFunc(rest, title)
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
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkChatur(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    await platformChecker(ChaturCas.isCassOnline, Notifications.ChaturNotification,Constants.casChatApiUrl,"chaturbate",rest)

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkOnlyfans(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    await platformChecker(OnlyCas.isCassOnline, Notifications.OFNotification,Constants.casOnlyUrl,"onlyfans",rest)

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkFansly(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    await platformChecker(FansCas.isCassOnline, Notifications.FansNotification,Constants.casFansUrl,"fansly",rest)

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkTwitch(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    await platformChecker(TwitchCas.isCassOnline, Notifications.TwitchNotification,Constants.casTwitchChannelName,"twitch",rest)

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkYT(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    await platformChecker(YouCas.isCassOnline, Notifications.YTNotification,Constants.casYtUrl,"youtube",rest)

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkKick(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    await platformChecker(KickCass.isCassOnline, Notifications.KickNotification,Constants.casKickUrl,"kick",rest)

@component.with_schedule
@tanjun.as_interval(Constants.longOnlineCheckTimer)
async def checkKittiesKick(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    await platformChecker(KickCass.isCassOnline, Notifications.KittiesKickNotification,Constants.kittiesKickUrl,"kittiesKick",rest)


@component.with_schedule
@tanjun.as_interval(Constants.avatarCheckTimer)
async def changeAvatar(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    db = Database()
    online = StaticMethods.checkOnline(db)
    onTime, offTime, totalOnTime = db.getStreamTableValues()
    hours, minutes = StaticMethods.timeToHoursMinutes(offTime)
    if online and not globals.normalAvtar:
        await rest.edit_my_user(avatar = 'plugins/avatars/calmCass.png')
        print("changed avatar to good cass")
        globals.normalAvtar = True
    if not online and globals.normalAvtar and hours >= Constants.MIN_TIME_BEFORE_AVATAR_CHANGE and offTime != 0:
        await rest.edit_my_user(avatar = 'plugins/avatars/missCass.png')
        print("changed avatar to bad cass")
        globals.normalAvtar = False

@component.with_schedule
@tanjun.as_interval(Constants.statusCheckTimer)
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
@tanjun.as_interval(Constants.statusCheckTimer)
async def checkOnlineTime() -> None:
    db = Database()
    online = StaticMethods.checkOnline(db)
    if online and globals.online != online:
        print("time online starts now")
        db.setStreamLastOnline(time.time())
        globals.online = online
    elif not online and globals.online != online:
        print("offline time starts now")
        globals.online = online
        db.setStreamLastOffline(time.time())
        lastOnline,lastOffline,lastTotalStreamLength = db.getStreamTableValues()
        newTotalStreamLength = lastTotalStreamLength + (lastOffline -  lastOnline)
        db.setStreamLastStreamLength(newTotalStreamLength)
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.restartCheckTimer)
async def checkRestart() -> None:
    db = Database()
    onTime,offTime,totalTime = db.getStreamTableValues()
    timeSinceRestart = time.time() - globals.botStartTime
    timeSinceOffline = time.time() - offTime
    if not globals.online and timeSinceRestart > Constants.TIME_BEFORE_BOT_RESTART and timeSinceOffline > Constants.TIME_OFFLINE_BEFORE_RESTART:
        StaticMethods.safeRebootServer()
    elif Constants.DEBUG:
        print("TimeSinceRestart: " + str(timeSinceRestart))
        print("TimeSinceOffline: " + str(timeSinceOffline))