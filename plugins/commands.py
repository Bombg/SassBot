import hikari.errors
import tanjun
import utils.StaticMethods as StaticMethods
import time
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
from utils.Database import Database
from datetime import datetime
from decorators.Permissions import Permissions
from decorators.CommandLogger import CommandLogger
from datetime import date
from datetime import timedelta
import utils.DataGrapher as DataGrapher
import hikari
import re
import utils.MiruViews as MiruViews
import alluka
import asyncio
from utils.EmbedCreator import EmbedCreator

component = tanjun.Component()

@component.with_slash_command
@tanjun.as_slash_command("ban-appeal", "Appeal a ban.", always_defer= True, default_to_ephemeral= True)
@CommandLogger
async def confess(ctx: tanjun.abc.SlashContext) -> None:
    view = MiruViews.AppealModalView(autodefer=False)
    await ctx.respond("Pre-type your ban appeal and then hit the submit button when you are ready to submit it.\n Button will time out after a few mins, so re-type command if it doesn't work", components=view)
    message = await ctx.fetch_last_response()
    await view.start(message)
    await view.wait()
    await ctx.interaction.delete_initial_response()

@component.with_slash_command
@tanjun.checks.with_check(StaticMethods.isPermission)
@tanjun.as_slash_command("appeal-review", "View appeals that need to be reviewd for approval or denial",default_to_ephemeral= True, always_defer= True)
async def appealReview(ctx: tanjun.abc.SlashContext, rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    db = Database()
    appealId,appeal, title = db.getUnreviewedAppeal()
    if appealId:
        view = MiruViews.AppealReView(appealId=appealId, tanCtx=ctx, appeal=appeal, rest=rest, title=title)
        content = f"## {appealId}:{title}\n``` {appeal} ```"
        await ctx.respond(content=content, components=view)
        message = await ctx.fetch_last_response()
        await view.start(message)
        await view.wait()
        message = await ctx.fetch_last_response()
        await ctx.interaction.delete_message(message)
    else:
        await ctx.respond("There are no appealss in need of review")

@component.with_slash_command
@tanjun.checks.with_check(StaticMethods.isPermission)
@tanjun.with_str_slash_option("channelid", "Text channel ID you wish to send a message to in order to test permissions")
@tanjun.as_slash_command("test-permission", "Test a notification for a specific platform",default_to_ephemeral= True, always_defer= True)
async def testNotification(ctx: tanjun.abc.SlashContext, rest: alluka.Injected[hikari.impl.RESTClientImpl], channelid:int) -> None:
    StaticMethods.logCommand("testNotification", ctx)
    messageContent = "Hooray, I can post here! Permissions looking good. Deleting this message after 60 seconds"
    embedMaker = EmbedCreator(
                                    f"{Constants.streamerName} is now live on test platform!", 
                                    "Test Title", 
                                    "https://www.google.com/", 
                                    'images/platformImages/twitchImage.png', 
                                    Constants.twitchEmbedColor, 
                                    Constants.defaultIcon, 
                                    "TestUserName"
                                )
    task = asyncio.create_task(embedMaker.getEmbed())
    try:
        testEmbed = await task
        message = await rest.create_message(channel = int(channelid), content = messageContent,embed=testEmbed)
        await ctx.respond("Success")
        await asyncio.sleep(60)
        await message.delete()
    except hikari.errors.ForbiddenError:
        await ctx.respond("Don't have permissions for this channel. Permissions Needed: View Channel, Post Messages, Embed Links.")

@component.with_slash_command
@tanjun.checks.with_check(StaticMethods.isPermission)
@tanjun.as_slash_command("confess-review", "View confessions that need to be reviewd for approval or denial",default_to_ephemeral= True, always_defer= True)
async def confessReview(ctx: tanjun.abc.SlashContext, rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    db = Database()
    confessionId,confession, title = db.getUnreviewedConfession()
    if confessionId:
        view = MiruViews.ConfessionReView(confessionId=confessionId, tanCtx=ctx, confession=confession, rest=rest, title=title)
        content = f"## {confessionId}:{title}\n``` {confession} ```"
        await ctx.respond(content=content, components=view)
        message = await ctx.fetch_last_response()
        await view.start(message)
        await view.wait()
        message = await ctx.fetch_last_response()
        await ctx.interaction.delete_message(message)
    else:
        await ctx.respond("There are no confessions in need of review")

@component.with_slash_command
@tanjun.as_slash_command("confess", "Anonymously post a confession or question to the confessions channel.", always_defer= True, default_to_ephemeral= True)
async def confess(ctx: tanjun.abc.SlashContext) -> None:
    view = MiruViews.ConfessionModalView(autodefer=False)
    await ctx.respond("Pre-type your Confession/Question and then hit the submit button when you are ready to submit it.\n Button will time out after a few mins, so re-type command if it doesn't work", components=view)
    message = await ctx.fetch_last_response()
    await view.start(message)
    await view.wait()
    await ctx.interaction.delete_initial_response()

@component.with_slash_command
@tanjun.with_bool_slash_option("rerunannounce","True if you want rerun pings False if not")
@tanjun.as_slash_command("announce-rerun-toggle", "Toggle whether or not the bot will announce reruns", default_to_ephemeral=True, always_defer=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def announceRerunToggle(ctx: tanjun.abc.SlashContext, rerunannounce:bool) -> None:
    db = Database()
    db.setRerunAnnounce(rerunannounce)
    onOff = "ON" if rerunannounce else "OFF"
    await ctx.respond(f"Rerun announcements have been turned {onOff}.")

@component.with_slash_command
@tanjun.with_str_slash_option("title", "The temporary title you wish to add")
@tanjun.with_str_slash_option("platform", "The platform you wish to add a temporary title for")
@tanjun.with_str_slash_option("accountname", "The account name for the platform you wish to create a temp title for. Optional if only 1 account", default="")
@tanjun.as_slash_command("title", "Add a temporary title for a platform", default_to_ephemeral=True, always_defer=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def tempTitle(ctx: tanjun.abc.SlashContext, title: str, platform: str, accountname: str) -> None:
    platforms = ['chaturbate','onlyfans','fansly','twitch','youtube','kick','cam4','mfc','bongacams', 'stripchat']
    db = Database()
    if platform.lower() in platforms:
        if not accountname:
            accounts = db.getPlatformAccountNames(platform)
            if len(accounts) == 1:
                accountname = accounts[0]
            elif len(accounts) == 0:
                await ctx.respond("No accounts for this platform in the database. Have you added this account in constants.py?")
            else:
                await ctx.respond(f"More than one account for this platform. You must input one from this list {accounts}")
        if accountname and db.doesAccountExist(platform, accountname):
            if title:
                db.addTempTitle(title,platform,accountname)
                await ctx.respond(f"sucessfully input the new temp title: '{title}'")
            else:
                await ctx.respond("Entered title is empty")
        else:
            await ctx.respond("Bad account name given")
    else:
        await ctx.respond(f"platform name input incorrectly. Use one from this list {platforms}")

@component.with_slash_command
@tanjun.as_slash_command("stream-stats", f"Get stats on how much {Constants.streamerName} has been streaming.", default_to_ephemeral=True, always_defer=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def streamStats(ctx: tanjun.abc.SlashContext) -> None:
    weekData = StaticMethods.getWeekStreamingMinutes(date.today())
    twoWeekData = StaticMethods.getWeekStreamingMinutes(date.today() - timedelta(days = 7), weekData)
    threeWeekData = StaticMethods.getWeekStreamingMinutes(date.today() - timedelta(days = 14), twoWeekData)
    fourWeekData = StaticMethods.getWeekStreamingMinutes(date.today() - timedelta(days = 21), threeWeekData)
    weekData = StaticMethods.replaceIntsWithString(weekData)
    twoWeekData = StaticMethods.replaceIntsWithString(twoWeekData)
    threeWeekData = StaticMethods.replaceIntsWithString(threeWeekData)
    fourWeekData = StaticMethods.replaceIntsWithString(fourWeekData)
    await ctx.respond(f"One Week Totals:{weekData}\nTwo Week Totals:{twoWeekData}\nFour Week Totals:{fourWeekData}\nChecks are made once every 10 min, so figures not exact")

@component.with_slash_command
@tanjun.with_str_slash_option("days", "Number of days back to include in the graph. Default is 1", default = 1)
@tanjun.with_str_slash_option("inputdate", "Date in yyyy-mm-dd format. If you don't enter anything today's date will be used", default = "")
@tanjun.as_slash_command("users-graph", "get agraph for the active users. Date in yyyy-mm-dd format, or todays date if no input.",default_to_ephemeral= True, always_defer=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def activeDailyUsersGraph(ctx: tanjun.abc.SlashContext, inputdate: str, days: int) -> None:
    if not inputdate:
        inputdate = str(date.today())
    restring = r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
    if re.search(restring, inputdate):
        db = Database()
        days = int(days)
        inputDateToDateTime = datetime.strptime(inputdate, '%Y-%m-%d').date()
        previousDate = inputDateToDateTime - timedelta(days = days - 1)
        isPresDateExists = db.isPresDateExists(inputdate)
        if isPresDateExists  and db.isPresDateExists(str(previousDate)):
            path = DataGrapher.createUserDayGraph(inputdate, days=days)
            file = hikari.File(path)
            await ctx.respond(file)
        else:
            errorString =f"There is no data for {inputdate}" if not isPresDateExists else f"There there is not enough data to go back to {previousDate}."
            await ctx.respond(errorString)
    else:
        await ctx.respond("Improper date format, use yyyy-mm-dd")

@component.with_slash_command
@tanjun.with_bool_slash_option("pingtruefalse", "True sets pings/everyone mentions on, False turns them off")
@tanjun.as_slash_command("ping-toggle", "Toggle for role pings in online announcements", default_to_ephemeral=True, always_defer=True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def togglePing(ctx: tanjun.abc.SlashContext, pingtruefalse: bool) -> None:
    db = Database()
    db.setPing(pingtruefalse)
    onOff = "ON" if pingtruefalse else "OFF"
    await ctx.respond(f"Role mention pings have been turned {onOff}.")

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
    await ctx.respond("Online Notifications should be resent when the next online check for each platform is made (could be a few minutes), assuming " + Constants.streamerName + " is online.")
    StaticMethods.setRebroadcast()

@component.with_slash_command
@tanjun.with_str_slash_option("imgurl", "Url of the image you wish to be embedded. Will also be pinned")
@tanjun.as_slash_command("rebroadcast-image", "Rebroadcast with a url, image will be embedded in the new announcement", default_to_ephemeral=True, always_defer= True)
@Permissions(Constants.whiteListedRoleIDs)
@CommandLogger
async def rebroadcastWithImage(ctx: tanjun.abc.SlashContext, imgurl: str) -> None:
    await ctx.respond(f"Added {imgurl} to the embed image list and will rebroadcast when the next online check is made. (could be minutes)")
    StaticMethods.pinImage(imgurl, Constants.PIN_TIME_SHORT)
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
    date = datetime.fromtimestamp(Constants.RECORD_KEEPING_START_DATE)
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
