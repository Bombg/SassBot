import tanjun
import globals
from multiprocessing.pool import ThreadPool
import StaticMethods


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

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())