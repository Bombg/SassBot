import tanjun
import alluka
import hikari
import asyncio
from ChaturCas import ChaturCas
from OnlyCas import OnlyCas
from FansCas import FansCas
from Constants import Constants
from TwitchCas import TwitchCas
from YouCas import YouCas
import globals
import time
from multiprocessing.pool import ThreadPool



component = tanjun.Component()
onlineCheckTimer = 180
avatarCheckTimer = 190
statusCheckTimer = 185


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())

@component.with_schedule
@tanjun.as_interval(onlineCheckTimer)
async def checkChatur(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    chaturbate = ChaturCas()
    task = asyncio.create_task(chaturbate.isCassOnline())
    isOnline = await task
    if isOnline:
        if globals.chaturFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("ChaturBoobies")
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.chaturOnlineText)
            globals.chaturFalse = 0
        globals.chaturFalse = globals.chaturFalse - 1
    else:
        if globals.chaturFalse < 0:
            globals.chaturFalse = 0
        globals.chaturFalse = globals.chaturFalse + 1
        print("ChaturbateOffline: " + str(globals.chaturFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(onlineCheckTimer)
async def checkOnlyfans(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    onlyFans = OnlyCas()
    task = asyncio.create_task(onlyFans.isCassOnline())
    isOnline = await task
    if isOnline:
        if globals.onlyFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("OnlyBoobies")
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.ofOnlineText)
            globals.onlyFalse = 0
        globals.onlyFalse = globals.onlyFalse - 1
    else:
        if globals.onlyFalse < 0:
            globals.onlyFalse = 0
        globals.onlyFalse = globals.onlyFalse + 1
        print("OnlyFansOffline: " + str(globals.onlyFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(onlineCheckTimer)
async def checkFansly(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    fans = FansCas()
    task = asyncio.create_task(fans.isCassOnline())
    isOnline = await task
    if isOnline:
        if globals.fansFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("FansBoobies")
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.fansOnlineText)
            globals.fansFalse = 0
        globals.fansFalse = globals.fansFalse - 1
    else:
        if globals.fansFalse < 0:
            globals.fansFalse = 0
        globals.fansFalse = globals.fansFalse + 1
        print("FanslyOffline: " + str(globals.fansFalse))
    print("\n")


@component.with_schedule
@tanjun.as_interval(onlineCheckTimer)
async def checkTwitch(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    twitch = TwitchCas()
    isOnline = twitch.isCassOnline()
    if isOnline:
        if globals.twitchFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("TwitchBoobies")
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.twitchOnlineText) 
            globals.twitchFalse = 0
        globals.twitchFalse = globals.twitchFalse - 1
    else:
        if globals.twitchFalse < 0:
            globals.twitchFalse = 0
        globals.twitchFalse = globals.twitchFalse + 1
        print("TwitchOffline: " + str(globals.twitchFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(onlineCheckTimer)
async def checkYT(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    youTube = YouCas()
    isOnline = youTube.isCassOnline()
    if isOnline:
        if globals.ytFalse >= Constants.WAIT_BETWEEN_MESSAGES:
            print("YTBoobies")
            await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.ytOnlineText)
            globals.ytFalse = 0
        globals.ytFalse = globals.ytFalse - 1
    else:
        if globals.ytFalse < 0:
            globals.ytFalse = 0
        globals.ytFalse = globals.ytFalse + 1
        print("YTOffline:" + str(globals.ytFalse))
    print("\n")

@component.with_schedule
@tanjun.as_interval(avatarCheckTimer)
async def changeAvatar(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if (globals.onlyFalse <= 0 or globals.chaturFalse <= 0) and (not globals.bad):
        print("Changed avatar to bad cat")
        await rest.edit_my_user(avatar = 'plugins/avatars/catEvil.png')
        globals.yawn = False
        globals.sleep = False
        globals.game = False
        globals.bad = True
    elif globals.fansFalse <= 0 and not globals.sleep and globals.onlyFalse > Constants.MIN_TIME_BEFORE_AVATAR_CHANGE and globals.chaturFalse > Constants.MIN_TIME_BEFORE_AVATAR_CHANGE:
        print("Changed avatar to sleeping cat")
        await rest.edit_my_user(avatar = 'plugins/avatars/catSleep.png')
        globals.sleep = True
        globals.yawn = False
        globals.game = False
        globals.bad = False
    elif not globals.yawn and globals.onlyFalse > Constants.MIN_TIME_BEFORE_AVATAR_CHANGE and globals.chaturFalse > Constants.MIN_TIME_BEFORE_AVATAR_CHANGE and globals.fansFalse > Constants.MIN_TIME_BEFORE_AVATAR_CHANGE and globals.twitchFalse > Constants.MIN_TIME_BEFORE_AVATAR_CHANGE and globals.ytFalse > Constants.MIN_TIME_BEFORE_AVATAR_CHANGE:
        print("Changed avatar to yawning cat")
        await rest.edit_my_user(avatar = 'plugins/avatars/catYawn.png')
        globals.yawn = True
        globals.sleep = False
        globals.game = False
        globals.bad = False
    elif not globals.game and globals.twitchFalse <= 0 or globals.ytFalse <= 0:
        print("Changed avatar to gaming cat")
        await rest.edit_my_user(avatar = 'plugins/avatars/catGame.png')
        globals.game = True
        globals.yawn = False
        globals.sleep = False
        globals.bad = False
    else:
        print("No change in avatar")
        print("sleep: " + str(globals.sleep))
        print("yawn: " + str(globals.yawn))
        print("game: " + str(globals.game))
        print("bad: " + str(globals.bad))
    print("\n")

@component.with_schedule
@tanjun.as_interval(statusCheckTimer)
async def changeStatus(bot: alluka.Injected[hikari.GatewayBot]) -> None:
    playingString = ""
    if globals.chaturFalse < 0:
        playingString = playingString + "CB "
    if globals.onlyFalse < 0:
        playingString = playingString + "OF "
    if globals.twitchFalse < 0:
        playingString = playingString + "Twitch "
    if globals.ytFalse < 0:
        playingString = playingString + "YT "
    if globals.sleep:
        playingString = playingString + "Fans "
    if globals.yawn and not playingString:
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
        print("yawn: " + str(globals.yawn))
        print("chaturFalse: " + str(globals.chaturFalse))
        print("onlyFalse: " + str(globals.chaturFalse))
        print("twitchFalse: " + str(globals.twitchFalse))
        print("ytFalse: " + str(globals.ytFalse))
        print("fansFalse: " + str(globals.fansFalse))
        print("Sleep: " + str(globals.sleep))
        print("bad: " + str(globals.bad))
    print("\n")

@component.with_schedule
@tanjun.as_interval(statusCheckTimer)
async def checkOnlineTime() -> None:
    online = checkOnline()
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
    
    

def checkOnline():
    online = False
    if globals.chaturFalse <= 0:
        online = True
    elif globals.onlyFalse <= 0:
        online = True
    elif globals.twitchFalse <= 0:
        online = True
    elif globals.ytFalse <= 0:
        online = True
    elif globals.fansFalse <= 0:
        online = True
    else:
        online = False
    return online

        