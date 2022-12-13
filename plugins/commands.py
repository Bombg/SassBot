import tanjun
import globals
import time
from multiprocessing.pool import ThreadPool


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
    if streamingOn == "":
        await ctx.respond("Cass isn't currently streaming")
    else:
        await ctx.respond("Cass is currently streaming on: \n " + streamingOn + "\n Links: https://linktr.ee/kitty_cass_")
    if globals.online:
        asyncResult = pool.apply_async(timeToHoursMinutes,(globals.onTime,))
        hours, minutes = asyncResult.get()
        await ctx.respond("Cass has been online for H:" + str(hours) + " M:" + str(minutes))
    else:
        asyncResult = pool.apply_async(timeToHoursMinutes,(globals.offTime,))
        hours, minutes = asyncResult.get()
        await ctx.respond("Cass has been offline for H:" + str(hours) + " M:" + str(minutes)) 

def timeToHoursMinutes(newTime):
    totalTime = time.time() - newTime
    totalTime = int(totalTime)
    #print(totalTime)
    totalTimeSeconds = int(totalTime % 60)
    #print(totalTimeSeconds)
    totalTimeMinutes = int((totalTime - totalTimeSeconds) / 60)
    leftoverMinutes = totalTimeMinutes % 60
    #print(totalTimeMinutes)
    totalTimeHours = int((totalTimeMinutes - leftoverMinutes ) / 60)

    return totalTimeHours, leftoverMinutes

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())