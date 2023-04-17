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
            globals.chaturLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.chaturOnlineText)
            globals.chaturFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongChaturBoobies")
            globals.chaturLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.chaturOnlineText)
        globals.chaturFalse = globals.chaturFalse - 1
    else:
        if globals.chaturFalse < 0:
            globals.chaturFalse = 0
        globals.chaturFalse = globals.chaturFalse + 1
        print("ChaturbateOffline: " + str(globals.chaturFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkOnlyfans(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    onlyFans = OnlyCas(Constants.casOnlyUrl)
    task = asyncio.create_task(onlyFans.isCassOnline())
    isOnline = await task
    secondsSinceLastMessage = StaticMethods.timeToSeconds(globals.fansLastOnlineMessage)
    if isOnline:
        if globals.onlyFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("OnlyBoobies")
            globals.onlyLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.ofOnlineText)
            globals.onlyFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongOnlyBoobies")
            globals.onlyLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.ofOnlineText)
        globals.onlyFalse = globals.onlyFalse - 1
    else:
        if globals.onlyFalse < 0:
            globals.onlyFalse = 0
        globals.onlyFalse = globals.onlyFalse + 1
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
            globals.fansLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.fansOnlineText)
            globals.fansFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongFansBoobies")
            globals.fansLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.fansOnlineText)
        globals.fansFalse = globals.fansFalse - 1
    else:
        if globals.fansFalse < 0:
            globals.fansFalse = 0
        globals.fansFalse = globals.fansFalse + 1
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
            globals.twitchLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.twitchOnlineText) 
            globals.twitchFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongTwitchBoobies")
            globals.twitchLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.twitchOnlineText)
        globals.twitchFalse = globals.twitchFalse - 1
    else:
        if globals.twitchFalse < 0:
            globals.twitchFalse = 0
        globals.twitchFalse = globals.twitchFalse + 1
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
            globals.ytLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.ytOnlineText)
            globals.ytFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongYTBoobies")
            globals.ytLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.ytOnlineText)
        globals.ytFalse = globals.ytFalse - 1
    else:
        if globals.ytFalse < 0:
            globals.ytFalse = 0
        globals.ytFalse = globals.ytFalse + 1
        print("YTOffline:" + str(globals.ytFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.onlineCheckTimer)
async def checkKick(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    kick = KickCass(Constants.casKickUrl)
    task = asyncio.create_task(kick.isCassOnline())
    isOnline = await task
    secondsSinceLastMessage = StaticMethods.timeToSeconds(globals.kickLastOnlineMessage)
    if isOnline == 3:
        # do nothing
        print("Kick check failed cause bot detection")
    elif isOnline == True:
        if globals.kickFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("KickBoobies")
            globals.kickLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.kickOnlineText)
            globals.kickFalse = 0
        elif secondsSinceLastMessage >= Constants.ONLINE_MESSAGE_REBROADCAST_TIME:
            print("LongKickBoobies")
            globals.kickLastOnlineMessage = time.time()
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.kickOnlineText)
        globals.kickFalse = globals.kickFalse - 1
    elif isOnline == False:
        if globals.kickFalse < 0:
            globals.kickFalse = 0
        globals.kickFalse = globals.kickFalse + 1
        print("KickOffline: " + str(globals.kickFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(Constants.avatarCheckTimer)
async def changeAvatar(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    online = StaticMethods.checkOnline()
    hours, minutes = StaticMethods.timeToHoursMinutes(globals.offTime)
    if online and not globals.normalAvtar:
        await rest.edit_my_user(avatar = 'plugins/avatars/calmCass.png')
        globals.normalAvtar = True
    if not online and globals.normalAvtar and hours >= Constants.MIN_TIME_BEFORE_AVATAR_CHANGE:
        await rest.edit_my_user(avatar = 'plugins/avatars/missCass.png')
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