import tanjun
import alluka
import hikari
import asyncio
from checkers.ChaturCas import ChaturCas
from checkers.OnlyCas import OnlyCas
from checkers.FansCas import FansCas
from Constants import Constants
from checkers.TwitchCas import TwitchCas
from checkers.KickCass import KickCass
from checkers.YouCas import YouCas
import globals
import time
import StaticMethods
from Notifications import Notifications
from Database import Database



component = tanjun.Component()


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkChatur(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    chaturbate = ChaturCas(Constants.casChatApiUrl)
    task = asyncio.create_task(chaturbate.isCassOnline())
    isOnline = await task
    db = Database()
    chaturLastOnlineMessage = db.getTableRowCol("platforms","chaturbate","last_online_message")
    secondsSinceLastMessage = StaticMethods.timeToSeconds(chaturLastOnlineMessage)
    if isOnline:
        if globals.chaturFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("ChaturBoobies")
            await Notifications.ChaturNotification(rest)
            db.updateTableRowCol("platforms","chaturbate","last_stream_start_time",time.time())
            globals.chaturFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongChaturBoobies")
            await Notifications.ChaturNotification(rest)
        chaturStreamStartTime = db.getTableRowCol("platforms","chaturbate","last_stream_start_time")
        secondsSinceStreamstart = StaticMethods.timeToSeconds(chaturStreamStartTime)
        globals.chaturFalse = -1 * secondsSinceStreamstart
    else:
        if globals.chaturFalse < 0:
            db.updateTableRowCol("platforms","chaturbate","last_stream_end_time",time.time())
            globals.chaturFalse = 0
        chaturStreamEndTime = db.getTableRowCol("platforms","chaturbate","last_stream_end_time")
        secondsSinceStreamEnd = StaticMethods.timeToSeconds(chaturStreamEndTime)
        globals.chaturFalse = secondsSinceStreamEnd
    if Constants.DEBUG:
        print("ChaturbateOffline: " + str(globals.chaturFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkOnlyfans(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    onlyFans = OnlyCas(Constants.casOnlyUrl)
    task = asyncio.create_task(onlyFans.isCassOnline())
    isOnline = await task
    db = Database()
    onlyLastOnlineMessage = db.getTableRowCol("platforms","onlyfans","last_online_message")
    secondsSinceLastMessage = StaticMethods.timeToSeconds(onlyLastOnlineMessage)
    if isOnline:
        if globals.onlyFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("OnlyBoobies")
            await Notifications.OFNotification(rest)
            db.updateTableRowCol("platforms","onlyfans","last_stream_start_time",time.time())
            globals.onlyFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongOnlyBoobies")
            await Notifications.OFNotification(rest)
        onlyStreamStartTime = db.getTableRowCol("platforms","onlyfans","last_stream_start_time")
        secondsSinceStreamStart = StaticMethods.timeToSeconds(onlyStreamStartTime)
        globals.onlyFalse = -1 * secondsSinceStreamStart
    else:
        if globals.onlyFalse < 0:
            db.updateTableRowCol("platforms","onlyfans","last_stream_end_time",time.time())
            globals.onlyFalse = 0
        onlyStreamEndTime = db.getTableRowCol("platforms","onlyfans","last_stream_end_time")
        secondsSinceStreamEnd = StaticMethods.timeToSeconds(onlyStreamEndTime)
        globals.onlyFalse = secondsSinceStreamEnd
    if Constants.DEBUG:
        print("OnlyFansOffline: " + str(globals.onlyFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkFansly(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    fans = FansCas(Constants.casFansUrl)
    task = asyncio.create_task(fans.isCassOnline())
    isOnline = await task
    db = Database()
    fansLastOnlineMessage = db.getTableRowCol("platforms","fansly","last_online_message")
    secondsSinceLastMessage = StaticMethods.timeToSeconds(fansLastOnlineMessage)
    if isOnline:
        if globals.fansFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("FansBoobies")
            await Notifications.FansNotification(rest)
            db.updateTableRowCol("platforms","fansly","last_stream_start_time",time.time())
            globals.fansFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongFansBoobies")
            await Notifications.FansNotification(rest)
        fansStreamStartTime = db.getTableRowCol("platforms","fansly","last_stream_start_time")
        secondsSinceStreamStart = StaticMethods.timeToSeconds(fansStreamStartTime)
        globals.fansFalse = -1 * secondsSinceStreamStart
    else:
        if globals.fansFalse < 0:
            db.updateTableRowCol("platforms","fansly","last_stream_end_time",time.time())
            globals.fansFalse = 0
        fansStreamEndTime = db.getTableRowCol("platforms","fansly","last_stream_end_time")
        secondsSinceStreamEnd = StaticMethods.timeToSeconds(fansStreamEndTime)
        globals.fansFalse = secondsSinceStreamEnd
    if Constants.DEBUG:
        print("FanslyOffline: " + str(globals.fansFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkTwitch(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    twitch = TwitchCas(Constants.casTwitchChannelName)
    isOnline = twitch.isCassOnline()
    db = Database()
    twitchLastOnlineMessage = db.getTableRowCol("platforms","twitch","last_online_message")
    secondsSinceLastMessage = StaticMethods.timeToSeconds(twitchLastOnlineMessage)
    if isOnline:
        if globals.twitchFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("TwitchBoobies")
            await Notifications.TwitchNotification(rest)
            db.updateTableRowCol("platforms","twitch","last_stream_start_time",time.time())
            globals.twitchFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongTwitchBoobies")
            await Notifications.TwitchNotification(rest)
        twitchStreamStartTime = db.getTableRowCol("platforms","twitch","last_stream_start_time")
        secondsSinceStreamStart = StaticMethods.timeToSeconds(twitchStreamStartTime)
        globals.twitchFalse = -1 * secondsSinceStreamStart
    else:
        if globals.twitchFalse < 0:
            db.updateTableRowCol("platforms","twitch","last_stream_end_time",time.time())
            globals.twitchFalse = 0
        twitchStreamEndTime = db.getTableRowCol("platforms","twitch","last_stream_end_time")
        secondsSinceStreamEnd = StaticMethods.timeToSeconds(twitchStreamEndTime)
        globals.twitchFalse = secondsSinceStreamEnd
    if Constants.DEBUG:
        print("TwitchOffline: " + str(globals.twitchFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkYT(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    youTube = YouCas(Constants.casYtUrl)
    isOnline = youTube.isCassOnline()
    db = Database()
    ytLastOnlineMessage = db.getTableRowCol("platforms","youtube","last_online_message")
    secondsSinceLastMessage = StaticMethods.timeToSeconds(ytLastOnlineMessage)
    if isOnline:
        if globals.ytFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("YTBoobies")
            await Notifications.YTNotification(rest)
            db.updateTableRowCol("platforms","youtube","last_stream_start_time",time.time())
            globals.ytFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongYTBoobies")
            await Notifications.YTNotification(rest)
        ytStreamStartTime = db.getTableRowCol("platforms","youtube","last_stream_start_time")
        secondsSinceStreamStartTime = StaticMethods.timeToSeconds(ytStreamStartTime)
        globals.ytFalse = -1 * secondsSinceStreamStartTime
    else:
        if globals.ytFalse < 0:
            db.updateTableRowCol("platforms","youtube","last_stream_end_time",time.time())
            globals.ytFalse = 0
        ytStreamEndTime = db.getTableRowCol("platforms","youtube","last_stream_end_time")
        secondsSinceStreamEndTime = StaticMethods.timeToSeconds(ytStreamEndTime)
        globals.ytFalse = secondsSinceStreamEndTime
    if Constants.DEBUG:
        print("YTOffline:" + str(globals.ytFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkKick(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    kick = KickCass(Constants.casKickUrl)
    task = asyncio.create_task(kick.isCassOnline())
    isOnline, title = await task
    db = Database()
    kickLastOnlineMessage = db.getTableRowCol("platforms","kick","last_online_message")
    secondsSinceLastMessage = StaticMethods.timeToSeconds(kickLastOnlineMessage)
    if isOnline == 3:
        # do nothing
        print("Kick check failed cause bot detection")
    elif isOnline == True:
        if globals.kickFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("KickBoobies")
            await Notifications.KickNotification(rest, title)
            db.updateTableRowCol("platforms","kick","last_stream_start_time",time.time())
            globals.kickFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongKickBoobies")
            await Notifications.KickNotification(rest, title)
        kickStreamStartTime = db.getTableRowCol("platforms","kick","last_stream_start_time")
        secondsSinceStreamStartTime = StaticMethods.timeToSeconds(kickStreamStartTime)
        globals.kickFalse = -1 * secondsSinceStreamStartTime
    elif isOnline == False:
        if globals.kickFalse < 0:
            db.updateTableRowCol("platforms","kick","last_stream_end_time",time.time())
            globals.kickFalse = 0
        kickStreamEndTime = db.getTableRowCol("platforms","kick","last_stream_end_time")
        secondsSinceStreamEndTime = StaticMethods.timeToSeconds(kickStreamEndTime)
        globals.kickFalse = secondsSinceStreamEndTime
    if Constants.DEBUG:
        print("KickOffline: " + str(globals.kickFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkKittiesKick(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    kick = KickCass(Constants.kittiesKickUrl)
    task = asyncio.create_task(kick.isCassOnline())
    isOnline, title = await task
    db = Database()
    kittiesKickLastOnlineMessage = db.getTableRowCol("platforms","kittiesKick","last_online_message")
    secondsSinceLastMessage = StaticMethods.timeToSeconds(kittiesKickLastOnlineMessage)
    if isOnline == 3:
        # do nothing
        print("Kick check failed cause bot detection")
    elif isOnline == True:
        if globals.kittiesKickFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("KickKitties")
            db.updateTableRowCol("platforms","kittiesKick","last_stream_start_time",time.time())
            globals.kittiesKickFalse = 0
            await Notifications.KittiesKickNotification(rest, title)
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongKickKitties")
            await Notifications.KittiesKickNotification(rest, title)
        kittiesStreamStartTime = db.getTableRowCol("platforms","kittiesKick","last_stream_start_time")
        secondsSinceStreamStartTime = StaticMethods.timeToSeconds(kittiesStreamStartTime)
        globals.kittiesKickFalse = -1 * secondsSinceStreamStartTime
    elif isOnline == False:
        if globals.kittiesKickFalse < 0:
            db.updateTableRowCol("platforms","kittiesKick","last_stream_end_time",time.time())
            globals.kittiesKickFalse = 0
        kittiesStreamEndTime = db.getTableRowCol("platforms","kittiesKick","last_stream_end_time")
        secondsSinceStreamEndTime = StaticMethods.timeToSeconds(kittiesStreamEndTime)
        globals.kittiesKickFalse = secondsSinceStreamEndTime
    if Constants.DEBUG:
        print("KittiesKickOffline: " + str(globals.kittiesKickFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.avatarCheckTimer)
async def changeAvatar(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    online = StaticMethods.checkOnline()
    db = Database()
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
    playingString = ""
    online = StaticMethods.checkOnline()
    db = Database()
    subathon,subStart,subEnd = db.getSubathonStatusClean()
    if globals.chaturFalse < 0:
        playingString = playingString + "CB "
    if globals.onlyFalse < 0:
        playingString = playingString + "OF "
    if globals.twitchFalse < 0:
        playingString = playingString + "Twitch "
    if globals.ytFalse < 0:
        playingString = playingString + "YT "
    if globals.fansFalse < 0:
        playingString = playingString + "Fans "
    if globals.kickFalse < 0:
        playingString = playingString + "Kick"
    if subathon:
        hours, minutes = StaticMethods.timeToHoursMinutes(subStart)
        playingString = playingString + "athon H:" + str(hours) + "M:" +str(minutes) + " "
    if not online and not playingString:
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
    else:
        print("No change in status")
        print("Online: " + str(online))
        print("chaturFalse: " + str(globals.chaturFalse))
        print("onlyFalse: " + str(globals.chaturFalse))
        print("twitchFalse: " + str(globals.twitchFalse))
        print("ytFalse: " + str(globals.ytFalse))
        print("fansFalse: " + str(globals.fansFalse))
        print("kickFalse: " + str(globals.kickFalse))
        print("KittiesFalse: " + str(globals.kittiesKickFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.statusCheckTimer)
async def checkOnlineTime() -> None:
    db = Database()
    online = StaticMethods.checkOnline()
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
    if not globals.online and timeSinceRestart > Constants.TIME_BEFORE_BOT_RESTART and timeSinceOffline > Constants.TIME_BEFORE_BOT_RESTART:
        StaticMethods.safeRebootServer()
    else:
        print("TimeSinceRestart: " + str(timeSinceRestart))
        print("TimeSinceOffline: " + str(timeSinceOffline))