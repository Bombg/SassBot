import tanjun
import globals
from multiprocessing.pool import ThreadPool
import StaticMethods
import time
from Constants import Constants
from Database import Database
from datetime import datetime
from decorators.Permissions import Permissions
import hikari

nl = "\n"
component = tanjun.Component()
pool = ThreadPool(processes=3)

@component.with_slash_command
@tanjun.as_slash_command("whats-my-id", "Find out what your User ID is!", default_to_ephemeral=True)
async def whats_my_id(ctx: tanjun.abc.Context) -> None:
    await ctx.respond(f"Hi {ctx.author.mention}! {nl} Your User ID is: ```{ctx.author.id}```")

@component.with_slash_command
@tanjun.as_slash_command("stream-status", "Find out what " +Constants.streamerName + " is currently doing", default_to_ephemeral=True)
async def streamStatus(ctx: tanjun.abc.Context) -> None:
    db = Database()
    lastOnline,lastOffline,totalStreamTime = db.getStreamTableValues()
    streamingOn = ""
    if globals.chaturFalse <= 0:
        streamingOn = streamingOn + "Chaturbate, "
    if globals.onlyFalse <= 0:
        streamingOn = streamingOn + "Onlyfans, "
    if globals.fansFalse <= 0:
        streamingOn = streamingOn + "Fansly, "
    if globals.ytFalse <= 0:
        streamingOn = streamingOn + "YouTube, "
    if globals.twitchFalse <= 0:
        streamingOn = streamingOn + "Twitch, "
    if globals.kickFalse <= 0:
        streamingOn = streamingOn + "Kick, "
    if streamingOn == "":
        if lastOffline == 0:
            await ctx.respond(Constants.streamerName + " isn't currently streaming , but check out her offline content! \n Links: "+ Constants.linkTreeUrl)
        else:
            asyncResult = pool.apply_async(StaticMethods.timeToHoursMinutes,(lastOffline,))
            hours, minutes = asyncResult.get()
            await ctx.respond(Constants.streamerName + " isn't currently streaming and has been offline for H:" + str(hours) + " M:" + str(minutes) + ", but check out her offline content! \n Links: "+ Constants.linkTreeUrl)
    else:
        asyncResult = pool.apply_async(StaticMethods.timeToHoursMinutes,(lastOnline,))
        hours, minutes = asyncResult.get()
        await ctx.respond(Constants.streamerName + " is currently streaming on: \n " + streamingOn + " and has been online for" + str(hours) + " M:" + str(minutes) + "\n Links: " + Constants.linkTreeUrl)
    tHours, tMinutes = StaticMethods.timeToHoursMinutesTotalTime(totalStreamTime)
    date = datetime.fromtimestamp(Constants.recordKeepingStartDate)
    await ctx.respond(Constants.streamerName + " has streamed a grand total of H:" + str(tHours) + " M:" + str(tMinutes) + " since records have been kept starting on " + str(date)) 

@component.with_slash_command
@tanjun.with_int_slash_option("epocstart", "The epoc time in seconds when the subathon started", default=0)
@tanjun.as_slash_command("subathon-start", "Start a subathon timer", default_to_ephemeral=True)
@Permissions(Constants.whiteListedRoleIDs)
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
async def rebootServer(ctx: tanjun.abc.Context)-> None:
    await ctx.respond("rebooting the server")
    StaticMethods.rebootServer()

@component.with_slash_command
@tanjun.as_slash_command("rebroadcast", "Resend online notification to your preset discord channel, assuming the streamer is online.", default_to_ephemeral=True)
@Permissions(Constants.whiteListedRoleIDs)
async def rebroadcast(ctx: tanjun.abc.Context) -> None:
    if globals.chaturFalse <= 0:
        globals.chaturRebroadcast = True
    if globals.onlyFalse <= 0:
        globals.onlyRebradcast = True
    if globals.fansFalse <= 0:
        globals.fansRebroadcast = True
    if globals.ytFalse <= 0:
        globals.ytRebroadcast = True
    if globals.twitchFalse <= 0:
        globals.twitchRebroadcast = True
    if globals.kickFalse <= 0:
        globals.kickRebroadcast = True
    await ctx.respond("Online Notifications should be resent soon, assuming " + Constants.streamerName + " is online.")

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
