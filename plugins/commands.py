import tanjun
import globals
from multiprocessing.pool import ThreadPool
import StaticMethods
import time
from Constants import Constants
from Database import Database
from datetime import datetime

nl = "\n"
component = tanjun.Component()
pool = ThreadPool(processes=3)


@component.with_slash_command
@tanjun.as_slash_command("whats-my-id", "Find out what your User ID is!", default_to_ephemeral=True)
async def whats_my_id(ctx: tanjun.abc.Context) -> None:
    await ctx.respond(f"Hi {ctx.author.mention}! {nl} Your User ID is: ```{ctx.author.id}```")

@component.with_slash_command
@tanjun.as_slash_command("stream-status", "Find out what cass is currently doing", default_to_ephemeral=True)
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
        asyncResult = pool.apply_async(StaticMethods.timeToHoursMinutes,(lastOffline,))
        hours, minutes = asyncResult.get()
        await ctx.respond("Cass isn't currently streaming and has been offline for H:" + str(hours) + " M:" + str(minutes) + ", but check out her offline content! \n Links: https://linktr.ee/kitty_cass_")
    else:
        asyncResult = pool.apply_async(StaticMethods.timeToHoursMinutes,(lastOnline,))
        hours, minutes = asyncResult.get()
        await ctx.respond("Cass is currently streaming on: \n " + streamingOn + " and has been online for" + str(hours) + " M:" + str(minutes) + "\n Links: https://linktr.ee/kitty_cass_")
    tHours, tMinutes = StaticMethods.timeToHoursMinutesTotalTime(totalStreamTime)
    date = datetime.fromtimestamp(1684210200)
    await ctx.respond("Cass has streamed a grand total of H:" + str(tHours) + " M:" + str(tMinutes) + " since records have been kept starting on " + str(date)) 

@component.with_slash_command
@tanjun.with_int_slash_option("epocstart", "The epoc time in seconds when the subathon started", default=0)
@tanjun.as_slash_command("subathon-start", "Start a subathon timer", default_to_ephemeral=True)
async def subathon_start(ctx: tanjun.abc.SlashContext, epocstart: int) -> None:
    db = Database()
    sub = db.getSubathonStatus()
    subathon = sub[0]
    if ctx.author.id in Constants.whiteListedIds and not subathon:
        await ctx.respond("Subathon timer has been set to epoc time " + str(epocstart))
        db.startSubathon(epocstart)
    elif not ctx.author.id in Constants.whiteListedIds:
        await ctx.respond("You aren't white listed for that")
    else:
        await ctx.respond("There's a subathon already running")

@component.with_slash_command
@tanjun.as_slash_command("subathon-end", "End a subathon timer", default_to_ephemeral=True)
async def subathon_end(ctx: tanjun.abc.Context)-> None:
    db = Database()
    subathon,subStart,subEndDontUse = db.getSubathonStatusClean()
    if ctx.author.id in Constants.whiteListedIds and subathon:
        await ctx.respond("Subathon timer has ended")
        subEnd = time.time()
        db.endSubathon(subEnd)
        longestSubLength = db.getSubathonLongest()
        currentSubLength = subEnd - subStart
        if currentSubLength > longestSubLength:
            db.setLongestSubathon(currentSubLength,subStart)
    elif not ctx.author.id in Constants.whiteListedIds:
        await ctx.respond("You aren't white listed for that")
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

@component.with_slash_command
@tanjun.as_slash_command("reboot", "reboot the bot and its server", default_to_ephemeral=True)
async def rebootServer(ctx: tanjun.abc.Context)-> None:
    if ctx.author.id in Constants.whiteListedIds:
        await ctx.respond("rebooting the server")
        StaticMethods.rebootServer()
    elif not ctx.author.id in Constants.whiteListedIds:
        await ctx.respond("You aren't white listed for that")


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
