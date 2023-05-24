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
    secondsSinceLastMessage = StaticMethods.timeToSeconds(globals.chaturLastOnlineMessage)
    if isOnline:
        if globals.chaturFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("ChaturBoobies")
            await Notifications.ChaturNotification(rest)
            globals.chaturStreamStartTime = time.time()
            globals.chaturFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongChaturBoobies")
            await Notifications.ChaturNotification(rest)
        secondsSinceStreamstart = StaticMethods.timeToSeconds(globals.chaturStreamStartTime)
        globals.chaturFalse = -1 * secondsSinceStreamstart
    else:
        if globals.chaturFalse < 0:
            globals.chaturStreamEndTime = time.time()
            globals.chaturFalse = 0
        secondsSinceStreamEnd = StaticMethods.timeToSeconds(globals.chaturStreamEndTime)
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
    secondsSinceLastMessage = StaticMethods.timeToSeconds(globals.onlyLastOnlineMessage)
    if isOnline:
        if globals.onlyFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("OnlyBoobies")
            await Notifications.OFNotification(rest)
            globals.onlyStreamStartTime = time.time()
            globals.onlyFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongOnlyBoobies")
            await Notifications.OFNotification(rest)
        secondsSinceStreamStart = StaticMethods.timeToSeconds(globals.onlyStreamStartTime)
        globals.onlyFalse = -1 * secondsSinceStreamStart
    else:
        if globals.onlyFalse < 0:
            globals.onlyStreamEndTime = time.time()
            globals.onlyFalse = 0
        secondsSinceStreamEnd = StaticMethods.timeToSeconds(globals.onlyStreamEndTime)
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
    secondsSinceLastMessage = StaticMethods.timeToSeconds(globals.fansLastOnlineMessage)
    if isOnline:
        if globals.fansFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("FansBoobies")
            await Notifications.FansNotification(rest)
            globals.fansStreamStartTime = time.time()
            globals.fansFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongFansBoobies")
            await Notifications.FansNotification(rest)
        secondsSinceStreamStart = StaticMethods.timeToSeconds(globals.fansStreamStartTime)
        globals.fansFalse = -1 * secondsSinceStreamStart
    else:
        if globals.fansFalse < 0:
            globals.fansStreamEndTime = time.time()
            globals.fansFalse = 0
        secondsSinceStreamEnd = StaticMethods.timeToSeconds(globals.fansStreamEndTime)
        globals.fansFalse = secondsSinceStreamEnd
    if Constants.DEBUG:
        print("FanslyOffline: " + str(globals.fansFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkTwitch(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    twitch = TwitchCas(Constants.casTwitchChannelName)
    isOnline = twitch.isCassOnline()
    secondsSinceLastMessage = StaticMethods.timeToSeconds(globals.twitchLastOnlineMessage)
    if isOnline:
        if globals.twitchFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("TwitchBoobies")
            await Notifications.TwitchNotification(rest)
            globals.twitchStreamStartTime = time.time()
            globals.twitchFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongTwitchBoobies")
            await Notifications.TwitchNotification(rest)
        secondsSinceStreamStart = StaticMethods.timeToSeconds(globals.twitchStreamStartTime)
        globals.twitchFalse = -1 * secondsSinceStreamStart
    else:
        if globals.twitchFalse < 0:
            globals.twitchStreamEndTime = time.time()
            globals.twitchFalse = 0
        secondsSinceStreamEnd = StaticMethods.timeToSeconds(globals.twitchStreamEndTime)
        globals.twitchFalse = secondsSinceStreamEnd
    if Constants.DEBUG:
        print("TwitchOffline: " + str(globals.twitchFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkYT(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    youTube = YouCas(Constants.casYtUrl)
    isOnline = youTube.isCassOnline()
    secondsSinceLastMessage = StaticMethods.timeToSeconds(globals.ytLastOnlineMessage)
    if isOnline:
        if globals.ytFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("YTBoobies")
            await Notifications.YTNotification(rest)
            globals.ytStreamStartTime = time.time()
            globals.ytFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongYTBoobies")
            await Notifications.YTNotification(rest)
        secondsSinceStreamStartTime = StaticMethods.timeToSeconds(globals.ytStreamStartTime)
        globals.ytFalse = -1 * secondsSinceStreamStartTime
    else:
        if globals.ytFalse < 0:
            globals.ytStreamEndTime = time.time()
            globals.ytFalse = 0
        secondsSinceStreamEndTime = StaticMethods.timeToSeconds(globals.ytStreamEndTime)
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
    secondsSinceLastMessage = StaticMethods.timeToSeconds(globals.kickLastOnlineMessage)
    if isOnline == 3:
        # do nothing
        print("Kick check failed cause bot detection")
    elif isOnline == True:
        if globals.kickFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("KickBoobies")
            await Notifications.KickNotification(rest, title)
            globals.kickStreamStartTime = time.time()
            globals.kickFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongKickBoobies")
            await Notifications.KickNotification(rest, title)
        secondsSinceStreamStartTime = StaticMethods.timeToSeconds(globals.kickStreamStartTime)
        globals.kickFalse = -1 * secondsSinceStreamStartTime
    elif isOnline == False:
        if globals.kickFalse < 0:
            globals.kickStreamEndTime = time.time()
            globals.kickFalse = 0
        secondsSinceStreamEndTime = StaticMethods.timeToSeconds(globals.kickStreamEndTime)
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
    secondsSinceLastMessage = StaticMethods.timeToSeconds(globals.kittiesKickLastOnlineMessage)
    if isOnline == 3:
        # do nothing
        print("Kick check failed cause bot detection")
    elif isOnline == True:
        if globals.kittiesKickFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("KickKitties")
            globals.kittiesStreamStartTime = time.time()
            globals.kittiesKickFalse = 0
            globals.kittiesKickLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.kittiesKickOnlineText)
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongKickKitties")
            globals.kittiesKickLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.kittiesKickOnlineText)
        secondsSinceStreamStartTime = StaticMethods.timeToSeconds(globals.kittiesStreamStartTime)
        globals.kittiesKickFalse = -1 * secondsSinceStreamStartTime
    elif isOnline == False:
        if globals.kittiesKickFalse < 0:
            globals.kittiesStreamEndTime = time.time()
            globals.kittiesKickFalse = 0
        secondsSinceStreamEndTime = StaticMethods.timeToSeconds(globals.kittiesStreamEndTime)
        globals.kittiesKickFalse = secondsSinceStreamEndTime
    if Constants.DEBUG:
        print("KittiesKickOffline: " + str(globals.kittiesKickFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.avatarCheckTimer)
async def changeAvatar(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    online = StaticMethods.checkOnline()
    hours, minutes = StaticMethods.timeToHoursMinutes(globals.offTime)
    if online and not globals.normalAvtar:
        await rest.edit_my_user(avatar = 'plugins/avatars/calmCass.png')
        print("changed avatar to good cass")
        globals.normalAvtar = True
    if not online and globals.normalAvtar and hours >= Constants.MIN_TIME_BEFORE_AVATAR_CHANGE and globals.offTime != 0:
        await rest.edit_my_user(avatar = 'plugins/avatars/missCass.png')
        print("changed avatar to bad cass")
        globals.normalAvtar = False

@component.with_schedule
@tanjun.as_interval(Constants.statusCheckTimer)
async def changeStatus(bot: alluka.Injected[hikari.GatewayBot]) -> None:
    playingString = ""
    online = StaticMethods.checkOnline()
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
    if globals.subathon:
        hours, minutes = StaticMethods.timeToHoursMinutes(globals.subathonStartTime)
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
    online = StaticMethods.checkOnline()
    if online and globals.online != online:
        print("time online starts now")
        globals.onTime = time.time()
        globals.offTime = 0
        globals.online = online
    elif not online and globals.online != online:
        print("offline time starts now")
        globals.online = online
        globals.offTime = time.time()
        globals.totalOnTime = globals.totalOnTime + (globals.offTime - globals.onTime)
        globals.onTime = 0
    elif globals.offTime == 0:
        globals.offTime = time.time()
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.restartCheckTimer)
async def checkRestart() -> None:
    timeSinceRestart = time.time() - globals.botStartTime
    timeSinceOffline = time.time() - globals.offTime
    if not globals.online and timeSinceRestart > Constants.TIME_BEFORE_BOT_RESTART and timeSinceOffline > Constants.TIME_BEFORE_BOT_RESTART:
        StaticMethods.safeRebootServer()
    else:
        print("TimeSinceRestart: " + str(timeSinceRestart))
        print("TimeSinceOffline: " + str(timeSinceOffline))