import tanjun
import StaticMethods
import time
from Constants import Constants
from Database import Database
from datetime import datetime
from decorators.Permissions import Permissions
from decorators.CommandLogger import CommandLogger

component = tanjun.Component()

@component.with_slash_command
@tanjun.with_bool_slash_option("pingtruefalse", "True sets pings/everyone mentions on, False turns them off")
@tanjun.as_slash_command("everyone-ping-toggle", "Toggle for @everyone pings in the announcements channel", default_to_ephemeral=True, always_defer=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def togglePing(ctx: tanjun.abc.SlashContext, pingtruefalse: bool) -> None:
    db = Database()
    db.setPing(pingtruefalse)
    onOff = "ON" if pingtruefalse else "OFF"
    await ctx.respond(f"Everyone mention pings have been turned {onOff}.")

@component.with_slash_command
@tanjun.as_slash_command("shutdown-bot", "Shut down the bot before restarting it so some info can be saved to the database", default_to_ephemeral= True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def shutDown(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("Shutting down the bot saving stuff to database before shtudown")
    StaticMethods.setOfflineAddTime()
    exit()

@component.with_slash_command
@tanjun.as_slash_command("image-check-pin", "Check to see if an image is pinned", default_to_ephemeral= True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def checkPin(ctx: tanjun.abc.SlashContext) -> None:
    url = StaticMethods.checkImagePin()
    if url:
        await ctx.respond(f"{url} is currently pinned")
    else:
        await ctx.respond("There is currently no image pinned")

@component.with_slash_command
@tanjun.as_slash_command("image-unpin", "if an image is pinned, it will be unpinned", default_to_ephemeral= True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def unPinImage(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("Unpinning any iamge that may be pinned")
    StaticMethods.unPin()

@component.with_slash_command
@tanjun.with_str_slash_option("imgurl", "Url of the image you wish to be pinned")
@tanjun.with_int_slash_option("hours", "number of hours you wish the image to be pinned for")
@tanjun.as_slash_command("image-pin", "set default embed image for set amount of time in hours", default_to_ephemeral=True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def pinImage(ctx: tanjun.abc.SlashContext, imgurl: str, hours: int) -> None:
    await ctx.respond(f"Pinning {imgurl} for {hours} hours")
    StaticMethods.pinImage(imgurl, hours)

@component.with_slash_command
@tanjun.as_slash_command("rebroadcast", "Resend online notification to your preset discord channel, assuming the streamer is online.", default_to_ephemeral=True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def rebroadcast(ctx: tanjun.abc.Context) -> None:
    await ctx.respond("Online Notifications should be resent within the next " + str(Constants.onlineCheckTimer) +  " seconds (or less), assuming " + Constants.streamerName + " is online.")
    StaticMethods.setRebroadcast()

@component.with_slash_command
@tanjun.with_str_slash_option("imgurl", "Url of the image you wish to be embedded. Will also be pinned")
@tanjun.as_slash_command("rebroadcast-image", "Rebroadcast with a url, image will be embedded in the new announcement", default_to_ephemeral=True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def rebroadcastWithImage(ctx: tanjun.abc.SlashContext, imgurl: str) -> None:
    await ctx.respond(f"Added {imgurl} to the embed image list and will rebroadcast within the next {Constants.onlineCheckTimer} seconds.")
    StaticMethods.pinImage(imgurl, Constants.pinTimeShort)
    StaticMethods.setRebroadcast()

@component.with_slash_command
@tanjun.as_slash_command("image-list-show", "Show urls of images that are on the list to be embedded", default_to_ephemeral=True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def showImgList(ctx: tanjun.abc.Context) -> None:
    db = Database()
    twImgList, twImgQue, bannedImages = db.getTwImgStuff()
    await ctx.respond(twImgList)

@component.with_slash_command
@tanjun.with_str_slash_option("url", "Url of the image you wish to be added to the image embed list")
@tanjun.as_slash_command("image-list-add", "Add an image to the list of images to be embedded", default_to_ephemeral=True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def addImgList(ctx: tanjun.abc.SlashContext, url: str) -> None:
    StaticMethods.addImageListQue(url)
    await ctx.respond(f"Added {url} to the embed image list")

@component.with_slash_command
@tanjun.with_str_slash_option("url", "Url of the image you wish to remove from the image embed list")
@tanjun.as_slash_command("image-list-remove", "Remove an image from the list of images that will be in embedded notifications", default_to_ephemeral=True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def remImgList(ctx: tanjun.abc.SlashContext, url: str) -> None:
    db = Database()
    twImgList, twImgQue, bannedList = db.getTwImgStuff()
    pinUrl = StaticMethods.checkImagePin()
    if pinUrl:
        StaticMethods.unPin()
    if url in twImgList:
        bannedList.append(url)
        db.setBannedList(bannedList)
        twImgList.remove(url)
        await ctx.respond(f"Removed {url} from the embed image list")
        db.setTwImgList(twImgList)
        if url in twImgQue:
            twImgQue.remove(url)
            db.setTwImgQueue(twImgQue)
    else:
        await ctx.respond(f"{url} could not be found in the image embed list. Nothing was removed.")

@component.with_slash_command
@tanjun.as_slash_command("stream-status", "Find out what " +Constants.streamerName + " is currently doing", default_to_ephemeral=True, always_defer= True)
@CommandLogger
async def streamStatus(ctx: tanjun.abc.Context) -> None:
    db = Database()
    lastOnline,lastOffline,totalStreamTime = db.getStreamTableValues()
    streamingOn = StaticMethods.checkOnline(db)
    if not streamingOn:
        if lastOffline == 0:
            await ctx.respond(Constants.streamerName + " isn't currently streaming , but check out her offline content! \n Links: "+ Constants.linkTreeUrl)
        else:
            hours, minutes = StaticMethods.timeToHoursMinutes(lastOffline)
            await ctx.respond(Constants.streamerName + " isn't currently streaming and has been offline for H:" + str(hours) + " M:" + str(minutes) + ", but check out her offline content! \n Links: "+ Constants.linkTreeUrl)
    else:
        hours, minutes = StaticMethods.timeToHoursMinutes(lastOnline)
        await ctx.respond(Constants.streamerName + " is currently streaming on: \n " + streamingOn + " and has been online for H:" + str(hours) + " M:" + str(minutes) + "\n Links: " + Constants.linkTreeUrl)
    tHours, tMinutes = StaticMethods.timeToHoursMinutesTotalTime(totalStreamTime)
    date = datetime.fromtimestamp(Constants.recordKeepingStartDate)
    await ctx.respond(Constants.streamerName + " has streamed a grand total of H:" + str(tHours) + " M:" + str(tMinutes) + " since records have been kept starting on " + str(date)) 

@component.with_slash_command
@tanjun.with_int_slash_option("epocstart", "The epoc time in seconds when the subathon started", default=0)
@tanjun.as_slash_command("subathon-start", "Start a subathon timer", default_to_ephemeral=True, always_defer= True)
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
@tanjun.as_slash_command("subathon-end", "End a subathon timer", default_to_ephemeral=True, always_defer= True)
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
@tanjun.as_slash_command("subathon", "See subathon status and time online", default_to_ephemeral=True, always_defer= True)
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
@tanjun.as_slash_command("reboot", "reboot the bot and its server", default_to_ephemeral=True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def rebootServer(ctx: tanjun.abc.Context)-> None:
    await ctx.respond("rebooting the server")
    StaticMethods.rebootServer()

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
