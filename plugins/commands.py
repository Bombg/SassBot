import tanjun
import globals
from multiprocessing.pool import ThreadPool
import StaticMethods
import time
from Constants import Constants
from Database import Database
from datetime import datetime
from decorators.Permissions import Permissions
from decorators.CommandLogger import CommandLogger
import asyncio

component = tanjun.Component()
pool = ThreadPool(processes=3)

@component.with_slash_command
@tanjun.as_slash_command("show-img-list", "Show urls of images that are on the list to be embedded", default_to_ephemeral=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def showImgList(ctx: tanjun.abc.Context) -> None:
    db = Database()
    twImgList, twImgQue = db.getTwImgStuff()
    await ctx.respond(twImgList)

@component.with_slash_command
@tanjun.with_str_slash_option("url", "Url of the image you wish to be added to the image embed list")
@tanjun.as_slash_command("add-img-list", "Add an image to the list of images to be embedded", default_to_ephemeral=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def addImgList(ctx: tanjun.abc.SlashContext, url: str) -> None:
    db = Database()
    twImgList, twImgQue = db.getTwImgStuff()
    twImgList.insert(0, url)
    db.setTwImgList(twImgList)
    twImgQue.insert(0,url)
    db.setTwImgQueue(twImgQue)
    await ctx.respond(f"Added {url} to the embed image list")

@component.with_slash_command
@tanjun.with_str_slash_option("url", "Url of the image you wish to remove from the image embed list")
@tanjun.as_slash_command("remove-img-list", "Remove an image from the list of images that will be in embedded notifications", default_to_ephemeral=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def remImgList(ctx: tanjun.abc.SlashContext, url: str) -> None:
    db = Database()
    twImgList, twImgQue = db.getTwImgStuff()
    if url in twImgList:
        twImgList.remove(url)
        await ctx.respond(f"Removed {url} from the embed image list")
        db.setTwImgList(twImgList)
        if url in twImgQue:
            twImgQue.remove(url)
            db.setTwImgQueue(twImgQue)
    else:
        await ctx.respond(f"{url} could not be found in the image embed list. Nothing was removed.")

@component.with_slash_command
@tanjun.as_slash_command("stream-status", "Find out what " +Constants.streamerName + " is currently doing", default_to_ephemeral=True)
@CommandLogger
async def streamStatus(ctx: tanjun.abc.Context) -> None:
    db = Database()
    lastOnline,lastOffline,totalStreamTime = db.getStreamTableValues()
    streamingOn = StaticMethods.checkOnline(db)
    if not streamingOn:
        if lastOffline == 0:
            await ctx.respond(Constants.streamerName + " isn't currently streaming , but check out her offline content! \n Links: "+ Constants.linkTreeUrl)
        else:
            asyncResult = pool.apply_async(StaticMethods.timeToHoursMinutes,(lastOffline,))
            hours, minutes = asyncResult.get()
            await ctx.respond(Constants.streamerName + " isn't currently streaming and has been offline for H:" + str(hours) + " M:" + str(minutes) + ", but check out her offline content! \n Links: "+ Constants.linkTreeUrl)
    else:
        asyncResult = pool.apply_async(StaticMethods.timeToHoursMinutes,(lastOnline,))
        hours, minutes = asyncResult.get()
        await ctx.respond(Constants.streamerName + " is currently streaming on: \n " + streamingOn + " and has been online for H:" + str(hours) + " M:" + str(minutes) + "\n Links: " + Constants.linkTreeUrl)
    tHours, tMinutes = StaticMethods.timeToHoursMinutesTotalTime(totalStreamTime)
    date = datetime.fromtimestamp(Constants.recordKeepingStartDate)
    await ctx.respond(Constants.streamerName + " has streamed a grand total of H:" + str(tHours) + " M:" + str(tMinutes) + " since records have been kept starting on " + str(date)) 

@component.with_slash_command
@tanjun.with_int_slash_option("epocstart", "The epoc time in seconds when the subathon started", default=0)
@tanjun.as_slash_command("subathon-start", "Start a subathon timer", default_to_ephemeral=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def subathon_start(ctx: tanjun.abc.SlashContext, epocstart: int) -> None:
    db = Database()
    sub = db.getSubathonStatus()
    subathon = sub[0]
    date = datetime.fromtimestamp(epocstart)
    if not subathon:
        await ctx.respond("Subathon timer has been set; starting at " + str(date))
        db.startSubathon(epocstart)
    else:
        await ctx.respond("There's a subathon already running")

@component.with_slash_command
@tanjun.as_slash_command("subathon-end", "End a subathon timer", default_to_ephemeral=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def subathon_end(ctx: tanjun.abc.Context)-> None:
    db = Database()
    subathon,subStart,subEndDontUse = db.getSubathonStatusClean()
    if subathon:
        await ctx.respond("Subathon timer has ended")
        subEnd = time.time()
        db.endSubathon(subEnd)
        longestSubLength = db.getSubathonLongest()
        currentSubLength = subEnd - subStart
        if currentSubLength > longestSubLength:
            db.setLongestSubathon(currentSubLength,subStart)
    else:
        await ctx.respond("There isn't a subathon to end")

@component.with_slash_command
@tanjun.as_slash_command("subathon", "See subathon status and time online", default_to_ephemeral=True)
@CommandLogger
async def subathon(ctx: tanjun.abc.Context)-> None:
    db = Database()
    subathon,subStart,subEnd = db.getSubathonStatusClean()
    longestSub, longestSubTime = db.getSubathonLongestTime()
    if subathon:
        hours, minutes = StaticMethods.timeToHoursMinutes(subStart)
        await ctx.respond("There is currently a subathon running that has been running for " + str(hours) + " hours, and " + str(minutes) + " minutes")
    elif subEnd > subStart:
        hours, minutes = StaticMethods.timeToHoursMinutesStartEnd(subStart, subEnd)
        lHours, lMinutes = StaticMethods.timeToHoursMinutesTotalTime(longestSub)
        date = datetime.fromtimestamp(longestSubTime)
        await ctx.respond("There currently isn't a subathon running but the last one ran for " + str(hours) + " hours, and " + str(minutes) + " minutes")
        await ctx.respond("The longest subathon ran for "+ str(lHours) + " hours, and " + str(lMinutes) + " minutes on " + str(date))
    elif subEnd == 0:
        await ctx.respond("There isn't a subathon running and a subathon hasn't been completed yet")

@component.with_slash_command
@tanjun.as_slash_command("reboot", "reboot the bot and its server", default_to_ephemeral=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def rebootServer(ctx: tanjun.abc.Context)-> None:
    await ctx.respond("rebooting the server")
    StaticMethods.rebootServer()

@component.with_slash_command
@tanjun.as_slash_command("rebroadcast", "Resend online notification to your preset discord channel, assuming the streamer is online.", default_to_ephemeral=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def rebroadcast(ctx: tanjun.abc.Context) -> None:
    globals.rebroadcast = True
    await ctx.respond("Online Notifications should be resent soon, assuming " + Constants.streamerName + " is online.")
    await asyncio.sleep(Constants.onlineCheckTimer)
    globals.rebroadcast = False

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
