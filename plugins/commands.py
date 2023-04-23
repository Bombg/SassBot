import tanjun
import globals
from multiprocessing.pool import ThreadPool
import StaticMethods
import time
from Constants import Constants

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
        await ctx.respond("Cass isn't currently streaming, but check out her offline content! \n Links: https://linktr.ee/kitty_cass_")
    else:
        await ctx.respond("Cass is currently streaming on: \n " + streamingOn + "\n Links: https://linktr.ee/kitty_cass_")
    if globals.online:
        asyncResult = pool.apply_async(StaticMethods.timeToHoursMinutes,(globals.onTime,))
        hours, minutes = asyncResult.get()
        await ctx.respond("Cass has been online for H:" + str(hours) + " M:" + str(minutes))
    else:
        asyncResult = pool.apply_async(StaticMethods.timeToHoursMinutes,(globals.offTime,))
        hours, minutes = asyncResult.get()
        await ctx.respond("Cass has been offline for H:" + str(hours) + " M:" + str(minutes)) 

@component.with_slash_command
@tanjun.with_int_slash_option("epocstart", "The epoc time in seconds when the subathon started", default=0)
@tanjun.as_slash_command("subathon-start", "Start a subathon timer", default_to_ephemeral=True)
async def subathon_start(ctx: tanjun.abc.SlashContext, epocstart: int) -> None:
    if ctx.author.id in Constants.whiteListedIds and not globals.subathon:
        await ctx.respond("Subathon timer has been set to epoc time " + str(epocstart))
        globals.subathon = True
        globals.subathonStartTime = epocstart
    elif not ctx.author.id in Constants.whiteListedIds:
        await ctx.respond("You aren't white listed for that")
    else:
        await ctx.respond("There's a subathon already running")

@component.with_slash_command
@tanjun.as_slash_command("subathon-end", "End a subathon timer", default_to_ephemeral=True)
async def subathon_end(ctx: tanjun.abc.Context)-> None:
    if ctx.author.id in Constants.whiteListedIds and globals.subathon:
        await ctx.respond("Subathon timer has ended")
        globals.subathon = False
        globals.subathonEndTime = time.time()
    elif not ctx.author.id in Constants.whiteListedIds:
        await ctx.respond("You aren't white listed for that")
    else:
        await ctx.respond("There isn't a subathon to end")

@component.with_slash_command
@tanjun.as_slash_command("subathon", "See subathon status and time online", default_to_ephemeral=True)
async def subathon(ctx: tanjun.abc.Context)-> None:
    if globals.subathon:
        hours, minutes = StaticMethods.timeToHoursMinutes(globals.subathonStartTime)
        await ctx.respond("There is currently a subathon running that has been running for " + str(hours) + " hours, and " + str(minutes) + " minutes")
    elif globals.subathonEndTime != 0:
        subathonTime = globals.subathonEndTime - globals.subathonStartTime
        hours, minutes = StaticMethods.timeToHoursMinutes(subathonTime)
        await ctx.respond("There currently isn't a subathon running but the last one ran for " + str(hours) + " hours, and " + str(minutes) + " minutes")

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
