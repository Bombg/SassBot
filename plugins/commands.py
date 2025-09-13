import hikari.errors
import tanjun
import utils.StaticMethods as StaticMethods
import time
from DefaultConstants import Settings as Settings
from utils.Database import Database
from datetime import datetime
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
import globals
import itertools
import miru
import logging

baseSettings = Settings()
component = tanjun.Component()
moderationGroup = tanjun.slash_command_group("zmod", "commands only moderators can use").add_check(StaticMethods.isPermission)
moderationGroupY = tanjun.slash_command_group("ymod", "commands only moderators can use").add_check(StaticMethods.isPermission )
logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

@tanjun.with_int_slash_option("days", "Number of days to look back", default=30)
@moderationGroupY.as_sub_command("kick-prefix-report", "Get most common emote prixes used in chat", default_to_ephemeral=True, always_defer=True)
@CommandLogger
async def KickPrefixLookUp(ctx: tanjun.abc.SlashContext, days:int) -> None:
    maxListLength = 1800
    db = Database()
    prefixes = db.GetAllEmotePrefixUsage(days)
    prefixList = ""
    for prefix, number in prefixes.items():
        prefixList += f"{prefix}:{number}" +"\n"
        if len(prefixList) > maxListLength:
            break
    await ctx.respond(content = prefixList)

@tanjun.with_str_slash_option("prefix", "prefix of the emote you want to check")
@tanjun.with_int_slash_option("days", "number of days to look back", default=30)
@moderationGroupY.as_sub_command("kick-emote-report", "Get stats on kick emotes of a given prefix", default_to_ephemeral=True, always_defer=True)
@CommandLogger
async def KickEmoteLookUp(ctx: tanjun.abc.SlashContext, prefix:str, days:int) -> None:
    if prefix and days:
        path = DataGrapher.GetEmoteStatsImage(prefix, days)
        file = hikari.File(path)
        await ctx.respond(file)
    else:
        await ctx.respond("bad input")

async def KickUserAutoCompelte(ctx: tanjun.abc.AutocompleteContext, value:str) -> None:
    db = Database()
    kickUsers = db.GetKickUsersAndId()
    choices = [
                name for name in kickUsers if value.lower() in name.lower()
            ]
    await ctx.set_choices({name: name for name in choices[:25]})

@component.with_slash_command
@tanjun.with_str_slash_option("author", "The username of the clip author you wish to search for", autocomplete=KickUserAutoCompelte)
@tanjun.with_int_slash_option("amount", "How many clips do you wish to see?", default=20)
@tanjun.as_slash_command("kick-clip-search-author", "Get clips by author", always_defer=True, default_to_ephemeral=True)
@CommandLogger
async def KickClipAuthorSearch(ctx: tanjun.abc.SlashContext, author:str, amount:int) -> None:
    if author:
        stepAmount = 20
        db = Database()
        clipIds = db.GetKickClipByAuthor(author)
        clipUrls = []
        urls = 0
        totalAmount = 0
        extra = 0
        for clipId in clipIds:
            clipUrls.append(StaticMethods.GetKickClipUrlFromClipId(clipId))
            urls += 1
            totalAmount += 1
            if urls == stepAmount and totalAmount < amount:
                await ctx.respond(clipUrls)
                clipUrls = []
                urls = 0
            elif totalAmount == amount and clipUrls:
                await ctx.respond(clipUrls)
            elif totalAmount > amount:
                extra += 1
        await ctx.respond(f"There's {extra} more entries. Use larger amount var to see more. Currently set to {amount}")
    else:
        await ctx.respond("improper input")

@moderationGroup.as_sub_command("confess-button", "A forever confess button to submit confessions", always_defer=True)
@CommandLogger
async def ConfessButton(ctx: tanjun.abc.SlashContext) -> None:
    view = MiruViews.ConfessButton()
    await ctx.respond(content = baseSettings.confessButtonMessage, components=view)
    message = await ctx.fetch_last_response()
    await view.start(message)
    await view.wait()

@moderationGroup.as_sub_command("ban-appeal-button", "A forever button that is pushed by users to appeal bans", always_defer=True)
@CommandLogger
async def BanAppealButton(ctx: tanjun.abc.SlashContext) -> None:
    view = MiruViews.BanAppealButton()
    await ctx.respond(content=baseSettings.banAppealButtonMessage, components=view,)
    message = await ctx.fetch_last_response()
    await view.start(message)
    await view.wait()

@moderationGroup.as_sub_command("kick-connect-button", "A forever button to connect kick accounts", always_defer= True)
@CommandLogger
async def ConnectKickButton(ctx: tanjun.abc.SlashContext) -> None:
    view = MiruViews.ConnectKick()
    content = baseSettings.kickConnectButtonMessage
    await ctx.respond(content=content, components=view)
    message = await ctx.fetch_last_response()
    await view.start(message)
    await view.wait()

async def KickClipAutoComplete(ctx: tanjun.abc.AutocompleteContext, value:str) -> None:
    db = Database()
    kickCLips = db.GetKickClipIdTitles()
    choices = {name: val for name,val in kickCLips.items() if value.lower() in name.lower()}
    await ctx.set_choices(dict(itertools.islice(choices.items(), 25)))

@component.with_slash_command
@tanjun.with_str_slash_option("title", "Title of the clip you're looking for",autocomplete=KickClipAutoComplete)
@tanjun.as_slash_command("kick-clip-search", "Search for a kick clip", default_to_ephemeral=True, always_defer=True)
@CommandLogger
async def SearchKickClips(ctx: tanjun.abc.SlashContext, title:str):
    if title:
        clipUrl = StaticMethods.GetKickClipUrlFromClipId(title)
        if clipUrl:
            await ctx.respond(clipUrl)
        else:
            ctx.respond("bad input")
    else:
        ctx.respond("bad input")


@tanjun.with_member_slash_option("member", "The member to select")
@moderationGroup.as_sub_command("kick-get-from-discord", "Get the Kick username for a specified Discord Username",default_to_ephemeral=True, always_defer=True)
@CommandLogger
async def GetDiscordKick(ctx: tanjun.abc.SlashContext, member: hikari.Member) -> None:
    db = Database()
    flag = True
    kickId = db.GetKickDiscordConnection(member.id)
    if not kickId: 
        flag = False
    kickSlug = db.GetKickSlugFromId(kickId)
    if kickSlug and flag:
        await ctx.respond(f"Kick Username: {kickSlug}")
    else:
        await ctx.respond("Couldn't find a Kick username attached to that Discord username")

@tanjun.with_int_slash_option("kickuserid","int id of the kick channel")
@tanjun.with_str_slash_option("eventname","name of the kick event", default="chat.message.sent")
@moderationGroup.as_sub_command("event-subscribe", "subscribe", always_defer= True, default_to_ephemeral= True)
@CommandLogger
async def eventSubscribe(ctx: tanjun.abc.SlashContext, kickuserid:int, eventname:str) -> None:
    import checkers.Kick as Kick
    Kick.subscribeWebhooks(kickuserid,eventname)
    await ctx.respond("This is a testing command. Nothin will show in discord")

@tanjun.with_member_slash_option("member", "The member to select.")
@tanjun.with_str_slash_option("kickuser", "Select Kick user.", autocomplete=KickUserAutoCompelte)
@moderationGroup.as_sub_command("kick-manual-connect", "MOD can connect Kick Account to Discord Account", always_defer=True, default_to_ephemeral=True)
@CommandLogger
async def ManualConnectKickAccount(ctx: tanjun.abc.SlashContext, member: hikari.Member, kickuser:str) -> None:
    db = Database()
    if member and kickuser:
        kickId = db.GetKickIdFromSlug(kickuser.lower())
        if kickId:
            db.insertDiscordKickAccountConnection(member.id,kickId)
            await ctx.respond(f"Inserted {kickuser}:{kickId} connected with {member.username}:{member.id}")
        else:
            import checkers.Kick as Kick
            info = Kick.getChannelInfoResponse([kickuser]).json()
            if info:
                kickId = info['data'][0]['broadcaster_user_id']
                db.insertKickUser(kickId,kickuser)
                db.insertDiscordKickAccountConnection(member.id,kickId)
                await ctx.respond(f"Inserted {kickuser}:{kickId} connected with {member.username}:{member.id}")
            else:
                await ctx.respond("User not in DB AND not found at API. Have them talk in Kick chat to be recorded OR enter their name correctly")
    else:
        await ctx.respond("bad data entry. Try again")

@CommandLogger
async def ConnectKickAccount(ctx: miru.ViewContext) -> None:
    if not baseSettings.kickClientId or not baseSettings.kickClientSecret:
        await ctx.respond("Kick API not set up")
        return
    codeVerifier = StaticMethods.GetCodeVerifier()
    oauthState = StaticMethods.GetOauthState()
    hashedVerifier = StaticMethods.GetHashedCodeVerifier(codeVerifier)
    codeChallenge = StaticMethods.GetCodeChallenge(hashedVerifier)
    discordId = ctx.member.id
    discordUsername = ctx.member.username
    db = Database()
    db.insertDiscordUser(discordId, discordUsername)
    stateIdVerifier = {oauthState:[discordId,codeVerifier]}
    globals.kickOauth.update(stateIdVerifier)
    kickOauthAuthorization = 'https://id.kick.com/oauth/authorize'
    redirectUrl = baseSettings.kickRedirectUrl
    params = {
                "client_id":baseSettings.kickClientId,
                "redirect_uri":redirectUrl,
                "response_type":"code",
                "scope":"user:read",
                "code_challenge":codeChallenge,
                "code_challenge_method":"S256",
                "state":oauthState
            }
    fullUrl = StaticMethods.EncodeParamsWithUrl(params, kickOauthAuthorization)
    view = MiruViews.DiscordKickConnectButton(fullUrl)
    await ctx.respond(components=view,flags=hikari.MessageFlag.EPHEMERAL)
    count = 0
    while oauthState in globals.kickOauth and count <= 300:
        count +=1
        await asyncio.sleep(2)
    await ctx.interaction.delete_initial_response()
    if oauthState not in globals.kickOauth:
        await ctx.respond("Success", flags=hikari.MessageFlag.EPHEMERAL)

@CommandLogger
async def BanAppeal(ctx: miru.ViewContext) -> None:
    if baseSettings.MOD_ROLE_ID and baseSettings.APPEAL_CHANNEL_ID:
        view = MiruViews.AppealModalView(autodefer=False)
        await ctx.respond("Pre-type your ban appeal and then hit the submit button when you are ready to submit it.\n Button will time out after a few mins, so re-push button if it doesn't work", components=view, flags=hikari.MessageFlag.EPHEMERAL)
        message = await ctx.get_last_response()
        await view.start(message)
        await view.wait()
        await ctx.interaction.delete_initial_response()
    else:
        await ctx.respond("Can't do that. Command isn't set up correctly. Tell an admin/mod", flags=hikari.MessageFlag.EPHEMERAL)
        logger.warning("BanAppeal can't be used. MOD_ROLE_ID and APPEAL_CHANNEL_ID not set")

@moderationGroupY.as_sub_command("appeal-review", "View appeals that need to be reviewd for approval or denial",default_to_ephemeral= True, always_defer= True)
@CommandLogger
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

@tanjun.with_str_slash_option("channelid", "Text channel ID you wish to send a message to in order to test permissions")
@moderationGroup.as_sub_command("test-permission", "Test a notification for a specific platform",default_to_ephemeral= True, always_defer= True)
@CommandLogger
async def testNotification(ctx: tanjun.abc.SlashContext, rest: alluka.Injected[hikari.impl.RESTClientImpl], channelid:int) -> None:
    StaticMethods.logCommand("testNotification", ctx)
    messageContent = "Hooray, I can post here! Permissions looking good. Deleting this message after 60 seconds"
    embedMaker = EmbedCreator(
                                    f"{baseSettings.streamerName} is now live on test platform!", 
                                    "Test Title", 
                                    "https://www.google.com/", 
                                    'images/platformImages/twitchImage.png', 
                                    baseSettings.twitchEmbedColor, 
                                    baseSettings.defaultIcon, 
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

@moderationGroupY.as_sub_command("confess-review", "View confessions that need to be reviewd for approval or denial",default_to_ephemeral= True, always_defer= True)
@CommandLogger
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
    if baseSettings.CONFESSTION_CHANNEL_ID:
        content = "Pre-type your Confession/Question and then hit the submit button when you are ready to submit it.\n Button will time out after a few mins, so re-type command if it doesn't work"
        view = MiruViews.ConfessionModalView(autodefer=False)
        if isinstance(ctx, tanjun.abc.SlashContext):
            await ctx.respond(content=content, components=view)
        else:
            await ctx.respond(content=content, components=view, flags = hikari.MessageFlag.EPHEMERAL)
        message = await ctx.fetch_last_response() if isinstance(ctx, tanjun.abc.SlashContext) else await ctx.get_last_response()
        await view.start(message)
        await view.wait()
        await ctx.interaction.delete_initial_response()
    else:
        logger.warning("CONFESS can't be uesed. CONFESSION_CHANNEL_ID not yet")
        if isinstance(ctx, tanjun.abc.SlashContext):
            await ctx.respond("Can't do that. Command isn't set up correctly. Tell admin/mod")
        else:
            await ctx.respond("Can't do that. Command isn't set up correctly. Tell admin/mod", flags = hikari.MessageFlag.EPHEMERAL)
@tanjun.with_bool_slash_option("rerunannounce","True if you want rerun pings False if not")
@moderationGroup.as_sub_command("announce-rerun-toggle", "Toggle whether or not the bot will announce reruns", default_to_ephemeral=True, always_defer=True)
@CommandLogger
async def announceRerunToggle(ctx: tanjun.abc.SlashContext, rerunannounce:bool) -> None:
    db = Database()
    db.setRerunAnnounce(rerunannounce)
    onOff = "ON" if rerunannounce else "OFF"
    await ctx.respond(f"Rerun announcements have been turned {onOff}.")

async def PlatformNameAutoComplete(ctx: tanjun.abc.AutocompleteContext, value:str) -> None:
    db = Database()
    platformNames = db.GetPlatformNames()
    await ctx.set_choices({name:name for name in platformNames if value.lower() in name.lower()})

@tanjun.with_str_slash_option("title", "The temporary title you wish to add")
@tanjun.with_str_slash_option("platform", "The platform you wish to add a temporary title for",autocomplete=PlatformNameAutoComplete)
@tanjun.with_str_slash_option("accountname", "The account name for the platform you wish to create a temp title for. Optional if only 1 account", default="")
@moderationGroup.as_sub_command("title", "Add a temporary title for a platform", default_to_ephemeral=True, always_defer=True)
@CommandLogger
async def tempTitle(ctx: tanjun.abc.SlashContext, title: str, platform: str, accountname: str) -> None:
    db = Database()
    platforms = db.GetPlatformNames()
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

@moderationGroup.as_sub_command("stream-stats", f"Get stats on how much {baseSettings.streamerName} has been streaming.", default_to_ephemeral=True, always_defer=True)
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

@tanjun.with_str_slash_option("days", "Number of days back to include in the graph. Default is 1", default = 1)
@tanjun.with_str_slash_option("inputdate", "Date in yyyy-mm-dd format. If you don't enter anything today's date will be used", default = "")
@moderationGroup.as_sub_command("users-graph", "get agraph for the active users. Date in yyyy-mm-dd format, or todays date if no input.",default_to_ephemeral= True, always_defer=True)
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

@tanjun.with_bool_slash_option("pingtruefalse", "True sets pings/everyone mentions on, False turns them off")
@moderationGroup.as_sub_command("ping-toggle", "Toggle for role pings in online announcements", default_to_ephemeral=True, always_defer=True)
@CommandLogger
async def togglePing(ctx: tanjun.abc.SlashContext, pingtruefalse: bool) -> None:
    db = Database()
    db.setPing(pingtruefalse)
    onOff = "ON" if pingtruefalse else "OFF"
    await ctx.respond(f"Role mention pings have been turned {onOff}.")

@moderationGroup.as_sub_command("shutdown-bot", "Shut down the bot before restarting it so some info can be saved to the database", default_to_ephemeral= True, always_defer= True)
@CommandLogger
async def shutDown(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("Shutting down the bot saving stuff to database before shtudown")
    StaticMethods.setOfflineAddTime()
    exit()

@moderationGroup.as_sub_command("image-check-pin", "Check to see if an image is pinned", default_to_ephemeral= True, always_defer= True)
@CommandLogger
async def checkPin(ctx: tanjun.abc.SlashContext) -> None:
    url = StaticMethods.checkImagePin()
    if url:
        await ctx.respond(f"{url} is currently pinned")
    else:
        await ctx.respond("There is currently no image pinned")

@moderationGroup.as_sub_command("image-unpin", "if an image is pinned, it will be unpinned", default_to_ephemeral= True, always_defer= True)
@CommandLogger
async def unPinImage(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("Unpinning any iamge that may be pinned")
    StaticMethods.unPin()

@tanjun.with_str_slash_option("imgurl", "Url of the image you wish to be pinned")
@tanjun.with_int_slash_option("hours", "number of hours you wish the image to be pinned for")
@moderationGroup.as_sub_command("image-pin", "set default embed image for set amount of time in hours", default_to_ephemeral=True, always_defer= True)
@CommandLogger
async def pinImage(ctx: tanjun.abc.SlashContext, imgurl: str, hours: int) -> None:
    await ctx.respond(f"Pinning {imgurl} for {hours} hours")
    StaticMethods.pinImage(imgurl, hours)

@moderationGroup.as_sub_command("rebroadcast", "Resend online notification to your preset discord channel, assuming the streamer is online.", default_to_ephemeral=True, always_defer= True)
@CommandLogger
async def rebroadcast(ctx: tanjun.abc.Context) -> None:
    await ctx.respond("Online Notifications should be resent when the next online check for each platform is made (could be a few minutes), assuming " + baseSettings.streamerName + " is online.")
    StaticMethods.setRebroadcast()

@tanjun.with_str_slash_option("imgurl", "Url of the image you wish to be embedded. Will also be pinned")
@moderationGroup.as_sub_command("rebroadcast-image", "Rebroadcast with a url, image will be embedded in the new announcement", default_to_ephemeral=True, always_defer= True)
@CommandLogger
async def rebroadcastWithImage(ctx: tanjun.abc.SlashContext, imgurl: str) -> None:
    await ctx.respond(f"Added {imgurl} to the embed image list and will rebroadcast when the next online check is made. (could be minutes)")
    StaticMethods.pinImage(imgurl, baseSettings.PIN_TIME_SHORT)
    StaticMethods.setRebroadcast()

@moderationGroup.as_sub_command("image-list-show", "Show urls of images that are on the list to be embedded", default_to_ephemeral=True, always_defer= True)
@CommandLogger
async def showImgList(ctx: tanjun.abc.Context) -> None:
    db = Database()
    twImgList, twImgQue, bannedImages = db.getTwImgStuff()
    await ctx.respond(twImgList)

@tanjun.with_str_slash_option("url", "Url of the image you wish to be added to the image embed list")
@moderationGroup.as_sub_command("image-list-add", "Add an image to the list of images to be embedded", default_to_ephemeral=True, always_defer= True)
@CommandLogger
async def addImgList(ctx: tanjun.abc.SlashContext, url: str) -> None:
    StaticMethods.addImageListQue(url)
    await ctx.respond(f"Added {url} to the embed image list")

@tanjun.with_str_slash_option("url", "Url of the image you wish to remove from the image embed list")
@moderationGroup.as_sub_command("image-list-remove", "Remove an image from the list of images that will be in embedded notifications", default_to_ephemeral=True, always_defer= True)
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
@tanjun.as_slash_command("stream-status", "Find out what " +baseSettings.streamerName + " is currently doing", default_to_ephemeral=True, always_defer= True)
@CommandLogger
async def streamStatus(ctx: tanjun.abc.Context) -> None:
    db = Database()
    lastOnline,lastOffline,totalStreamTime = db.getStreamTableValues()
    streamingOn = StaticMethods.checkOnline(db)
    if not streamingOn:
        if lastOffline == 0:
            await ctx.respond(baseSettings.streamerName + " isn't currently streaming , but check out her offline content! \n Links: "+ baseSettings.linkTreeUrl)
        else:
            hours, minutes = StaticMethods.timeToHoursMinutes(lastOffline)
            await ctx.respond(baseSettings.streamerName + " isn't currently streaming and has been offline for H:" + str(hours) + " M:" + str(minutes) + ", but check out her offline content! \n Links: "+ baseSettings.linkTreeUrl)
    else:
        hours, minutes = StaticMethods.timeToHoursMinutes(lastOnline)
        await ctx.respond(baseSettings.streamerName + " is currently streaming on: \n " + streamingOn + " and has been online for H:" + str(hours) + " M:" + str(minutes) + "\n Links: " + baseSettings.linkTreeUrl)
    tHours, tMinutes = StaticMethods.timeToHoursMinutesTotalTime(totalStreamTime)
    date = datetime.fromtimestamp(baseSettings.RECORD_KEEPING_START_DATE)
    await ctx.respond(baseSettings.streamerName + " has streamed a grand total of H:" + str(tHours) + " M:" + str(tMinutes) + " since records have been kept starting on " + str(date)) 

@tanjun.with_int_slash_option("epocstart", "The epoc time in seconds when the subathon started", default=0)
@moderationGroup.as_sub_command("subathon-start", "Start a subathon timer", default_to_ephemeral=True, always_defer= True)
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

@moderationGroup.as_sub_command("subathon-end", "End a subathon timer", default_to_ephemeral=True, always_defer= True)
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

@moderationGroup.as_sub_command("reboot", "reboot the bot and its server", default_to_ephemeral=True, always_defer= True)
@CommandLogger
async def rebootServer(ctx: tanjun.abc.Context)-> None:
    await ctx.respond("rebooting the server")
    StaticMethods.rebootServer()

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    compCopy = component.copy()
    compCopy = compCopy.add_slash_command(moderationGroup)
    compCopy = compCopy.add_slash_command(moderationGroupY)
    client.add_component(compCopy)
