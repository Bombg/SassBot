import hikari.errors
import tanjun
import alluka
import hikari
import asyncio
import checkers.Chaturbate as Chaturbate
import checkers.Onlyfans as Onlyfans
import checkers.Fansly as Fansly
import checkers.Myfreecams as MFC
import checkers.Bongacams as BC
import checkers.Stripchat as SC
import checkers.Eplay as EP
import checkers.Manyvids as MV
from DefaultConstants import Settings as Settings
import checkers.Twitch as Twitch
import checkers.Kick as Kick
import checkers.Youtube as Youtube
import checkers.Cam4 as Cam4
import globals
import time
import utils.StaticMethods as StaticMethods
from utils.Notifications import Notifications
from utils.Database import Database
from typing import Callable
from datetime import date
import inspect
import logging
import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
import json
import datetime
import utils.KickDataGrabber as KickDataGrabber
import requests

baseSettings = Settings()
component = tanjun.Component()
logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())

async def platformChecker(isOnlineFunc: Callable,platformNotifFunc: Callable, userName: str, platformName: str, rest: hikari.impl.RESTClientImpl):
    try:
        if inspect.iscoroutinefunction(isOnlineFunc):
            isOnline, title, thumbUrl, icon = await isOnlineFunc(userName)
            globals.lastNoDriverCheckTime = time.time()
        else:
            isOnline, title, thumbUrl, icon = await asyncio.get_running_loop().run_in_executor(None,isOnlineFunc,userName)
            globals.lastCheckTime = time.time()
    except Exception as e:
        logging.exception(f"caught exception: {e}")
        thumbUrl = ""
        title = "NoTitle"
        isOnline = False
        icon = baseSettings.defaultIcon
    isRerun = False
    db = Database()
    lastOnlineMessage,streamStartTime,streamEndTime = db.getPlatformAccountsRowValues(platformName,userName)
    tempTitle, tempTitleTime = db.getPlatformTempTitle(platformName, userName)
    secondsSinceTempTitle = StaticMethods.timeToSeconds(tempTitleTime)
    secondsSinceLastMessage = StaticMethods.timeToSeconds(lastOnlineMessage)
    secondsSinceStreamEndTime = StaticMethods.timeToSeconds(streamEndTime)
    secondsSinceStreamStartTime = StaticMethods.timeToSeconds(streamStartTime)
    if tempTitle and secondsSinceTempTitle < baseSettings.TEMP_TITLE_UPTIME:
        title = tempTitle
    if isOnline and StaticMethods.isRerun(title):
        isOnline = isOnline if db.getRerunAnnounce() else False
        isRerun = True
    logger.debug(platformName + " +Offline|-Online: " + str((-1 * secondsSinceStreamStartTime) if isOnline else secondsSinceStreamEndTime))
    if isOnline:
        db.setRerun(isRerun, platformName)
        if secondsSinceStreamEndTime >= baseSettings.WAIT_BETWEEN_MESSAGES and secondsSinceLastMessage >= baseSettings.WAIT_BETWEEN_MESSAGES and streamEndTime >= streamStartTime:
            logger.info(f"{platformName}: Sending Notification")
            await platformNotifFunc(rest, title, thumbUrl, icon, userName, isRerun)
            db.SetPlatformLastStreamStartTime(platformName,time.time())
            db.SetPlatformAccountLastStreamStartTime(platformName, userName,time.time())
            globals.rebroadcast[platformName] = 0
        elif secondsSinceLastMessage >= baseSettings.ONLINE_MESSAGE_REBROADCAST_TIME or globals.rebroadcast[platformName]:
            logger.info(f"{platformName}: Rebroadcast Command or Rebroadcast_TIME Notification sent")
            await platformNotifFunc(rest, title, thumbUrl, icon, userName, isRerun)
            lastOnlineMessage = time.time()
            globals.rebroadcast[platformName] = 0
        elif streamEndTime >= streamStartTime:
            db.SetPlatformLastStreamStartTime(platformName,time.time())
            db.SetPlatformAccountLastStreamStartTime(platformName,userName,time.time())
    elif not isOnline:
        db.setRerun(isRerun, platformName)
        if streamEndTime <= streamStartTime:
            db.SetPlatformLastStreamEndTime(platformName,time.time())
            db.SetPlatformAccountLastStreamEndTime(platformName,userName,time.time())
        globals.rebroadcast[platformName] = 0

@component.with_schedule
@tanjun.as_interval(baseSettings.CB_CHECK_TIMER)
async def checkChatur(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.cbUserName:
        for cbUserName in baseSettings.cbUserName:
            await platformChecker(Chaturbate.isModelOnline, Notifications.ChaturNotification,cbUserName,"chaturbate",rest)
            await asyncio.sleep(baseSettings.CB_CHECK_TIMER/len(baseSettings.cbUserName))

@component.with_schedule
@tanjun.as_interval(baseSettings.OF_CHECK_TIMER)
async def checkOnlyfans(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.ofUserName:
        for ofUserName in baseSettings.ofUserName:
            await platformChecker(Onlyfans.isModelOnline, Notifications.OFNotification,ofUserName,"onlyfans",rest)
            await asyncio.sleep(baseSettings.OF_CHECK_TIMER/len(baseSettings.ofUserName))

@component.with_schedule
@tanjun.as_interval(baseSettings.FANS_CHECK_TIMER)
async def checkFansly(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.fansUserName:
        for fansUserName in baseSettings.fansUserName:
            await platformChecker(Fansly.isModelOnline, Notifications.FansNotification,fansUserName,"fansly",rest)
            await asyncio.sleep(baseSettings.FANS_CHECK_TIMER/len(baseSettings.fansUserName))

@component.with_schedule
@tanjun.as_interval(baseSettings.TWITCH_CHECK_TIMER)
async def checkTwitch(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.twitchUserName:
        for twitchUserName in baseSettings.twitchUserName:
            await platformChecker(Twitch.isModelOnline, Notifications.TwitchNotification,twitchUserName,"twitch",rest)
            await asyncio.sleep(baseSettings.TWITCH_CHECK_TIMER/len(baseSettings.twitchUserName))

@component.with_schedule
@tanjun.as_interval(baseSettings.YT_CHECK_TIMER)
async def checkYT(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.ytUserName:
        for ytUserName in baseSettings.ytUserName:
            await platformChecker(Youtube.isModelOnline, Notifications.YTNotification,ytUserName,"youtube",rest)
            await asyncio.sleep(baseSettings.YT_CHECK_TIMER/len(baseSettings.ytUserName))

@component.with_schedule
@tanjun.as_interval(baseSettings.KICK_CHECK_TIMER)
async def checkKick(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.kickClientId:
        kickOnlineFunc = Kick.isModelOnlineAPI
        await asyncio.sleep(1)
    else:
        kickOnlineFunc = Kick.isModelOnline
    if baseSettings.kickUserName:
        for kickUserName in baseSettings.kickUserName:
            await platformChecker(kickOnlineFunc, Notifications.KickNotification,kickUserName,"kick",rest)
            await asyncio.sleep(baseSettings.KICK_CHECK_TIMER/len(baseSettings.kickUserName)%baseSettings.KICK_CHECK_TIMER)

@component.with_schedule
@tanjun.as_interval(baseSettings.CAM4_CHECK_TIMER)
async def checkCam4(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.cam4UserName:
        for cam4UserName in baseSettings.cam4UserName:
            await platformChecker(Cam4.isModelOnline, Notifications.Cam4Notification,cam4UserName,"cam4",rest)
            await asyncio.sleep(baseSettings.CAM4_CHECK_TIMER/len(baseSettings.cam4UserName))

@component.with_schedule
@tanjun.as_interval(baseSettings.MFC_CHECK_TIMER)
async def checkMfc(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.mfcUserName:
        for mfcUserName in baseSettings.mfcUserName:
            await platformChecker(MFC.isModelOnline, Notifications.MfcNotification,mfcUserName,"mfc",rest)
            await asyncio.sleep(baseSettings.MFC_CHECK_TIMER/len(baseSettings.mfcUserName))


@component.with_schedule
@tanjun.as_interval(baseSettings.BC_CHECK_TIMER)
async def checkBc(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.bcUserName:
        for bcUserName in baseSettings.bcUserName:
            await platformChecker(BC.isModelOnline, Notifications.BcNotification,bcUserName,"bongacams",rest)
            await asyncio.sleep(baseSettings.BC_CHECK_TIMER/len(baseSettings.bcUserName))


@component.with_schedule
@tanjun.as_interval(baseSettings.SC_CHECK_TIMER)
async def checkSc(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.scUserName:
        for scUserName in baseSettings.scUserName:
            await platformChecker(SC.isModelOnline, Notifications.ScNotification,scUserName,"stripchat",rest)
            await asyncio.sleep(baseSettings.SC_CHECK_TIMER/len(baseSettings.scUserName))

@component.with_schedule
@tanjun.as_interval(baseSettings.EP_CHECK_TIMER)
async def checkEp(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.epUserName:
        for epUserName in baseSettings.epUserName:
            await platformChecker(EP.isModelOnline, Notifications.EpNotification,epUserName,"eplay",rest)
            await asyncio.sleep(baseSettings.EP_CHECK_TIMER/len(baseSettings.epUserName))

@component.with_schedule
@tanjun.as_interval(baseSettings.MV_CHECK_TIMER)
async def checkMv(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if baseSettings.mvUserName:
        for mvUserName in baseSettings.mvUserName:
            await platformChecker(MV.isModelOnline, Notifications.MvNotification,mvUserName,"manyvids",rest)
            await asyncio.sleep(baseSettings.MV_CHECK_TIMER/len(baseSettings.mvUserName))


@component.with_schedule
@tanjun.as_interval(baseSettings.AVATAR_CHECK_TIMER)
async def changeAvatar(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    db = Database()
    online = StaticMethods.checkOnline(db)
    onTime, offTime, totalOnTime = db.getStreamTableValues()
    hours, minutes = StaticMethods.timeToHoursMinutes(offTime)
    if online and not globals.normalAvtar:
        await rest.edit_my_user(avatar = baseSettings.calmAvatar)
        logger.info(f"changed avatar to good {baseSettings.streamerName}")
        globals.normalAvtar = True
    if not online and globals.normalAvtar and hours >= baseSettings.MIN_TIME_BEFORE_AVATAR_CHANGE and offTime != 0:
        await rest.edit_my_user(avatar = baseSettings.pissedAvatar)
        logger.info(f"changed avatar to bad {baseSettings.streamerName}")
        globals.normalAvtar = False

@component.with_schedule
@tanjun.as_interval(baseSettings.STATUS_CHECK_TIMER)
async def changeStatus(bot: alluka.Injected[hikari.GatewayBot]) -> None:
    db = Database()
    subathon,subStart,subEnd = db.getSubathonStatusClean()
    playingString = StaticMethods.checkOnline(db)
    if subathon:
        hours, minutes = StaticMethods.timeToHoursMinutes(subStart)
        playingString = playingString + "athon H:" + str(hours) + "M:" +str(minutes) + " "
    if not playingString:
        playingString = playingString + "Offline "
    if playingString != globals.globalPlayString:
        logger.info("Updated presence to " + playingString)
        globals.globalPlayString = playingString
        await asyncio.sleep(5)
        await bot.update_presence(activity=hikari.Activity(
            name = playingString, 
            type = hikari.ActivityType.STREAMING, 
            url = baseSettings.twitchUrl
            ))
        await asyncio.sleep(5)

@component.with_schedule
@tanjun.as_interval(baseSettings.STATUS_CHECK_TIMER)
async def checkOnlineTime() -> None:
    db = Database()
    online = StaticMethods.checkOnline(db)
    lastOnline,lastOffline,totalStreamTime = db.getStreamTableValues()
    if online and lastOffline >= lastOnline:
        logger.info("time online starts now")
        db.setStreamLastOnline(time.time())
    elif not online and lastOffline <= lastOnline:
        logger.info("offline time starts now")
        StaticMethods.setOfflineAddTime()

@component.with_schedule
@tanjun.as_time_schedule(minutes=[5,15,25,35,45,55])
async def checkRestart() -> None:
    db = Database()
    onTime,offTime,totalTime = db.getStreamTableValues()
    online = StaticMethods.checkOnline(db)
    timeSinceRestart = time.time() - globals.botStartTime
    timeSinceOffline = time.time() - offTime
    if not online and timeSinceRestart > baseSettings.TIME_BEFORE_BOT_RESTART and timeSinceOffline > baseSettings.TIME_OFFLINE_BEFORE_RESTART:
        StaticMethods.safeRebootServer()
        logger.debug("TimeSinceRestart: " + str(timeSinceRestart))
        logger.debug("TimeSinceOffline: " + str(timeSinceOffline))

@component.with_schedule
@tanjun.as_time_schedule(minutes=[0,10,20,30,40,50])
async def presenceGrabber(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    members = rest.fetch_members(baseSettings.GUILD_ID)
    db = Database()
    online = StaticMethods.checkOnline(db)
    presencesDict = db.getPresenceDay(date.today())
    hourMinute = StaticMethods.getHourMinuteString()
    statusCounts = {}
    memberCount = 0
    if online:
        statusCounts["streaming"] = online
    async for member in members:
        memberCount += 1
        presence = member.get_presence()
        if presence is not None:
            status = presence.visible_status
            statusStr = str(status)
            if statusStr in statusCounts:
                statusCounts[statusStr] += 1
            else:
                statusCounts[statusStr] = 1
    statusCounts["members"] = memberCount
    presencesDict[hourMinute] = statusCounts
    db.setPresenceDay(date.today(), presencesDict)

@component.with_schedule
@tanjun.as_time_schedule(minutes = [1,11,21,31,41,51])
async def smartAlert(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    db = Database()
    presencesDict = db.getPresenceDay(date.today())
    lastWeekPresenceDict = db.getLastWeeksDayPresenceData(date.today())
    hourMinute = StaticMethods.getHourMinuteString()
    lookAheadHourMinute = StaticMethods.getHourMinuteString(offset=baseSettings.SMART_ALERT_LOOK_AHEAD)
    if lastWeekPresenceDict:
        maxOnlineLastWeek = StaticMethods.getMaxOnlineInPresenceDict(lastWeekPresenceDict)
        if presencesDict[hourMinute] and lastWeekPresenceDict[lookAheadHourMinute]:
            lookAheadOnline = lastWeekPresenceDict[lookAheadHourMinute]['online']
            nowOnline = presencesDict[hourMinute]['online']
            onlineThreshold = int(maxOnlineLastWeek * baseSettings.PERCENTAGE_OF_MAX)
            if nowOnline >= onlineThreshold and lookAheadOnline >= onlineThreshold:
                StaticMethods.smartRebroadcast()

@component.with_schedule
@tanjun.as_interval(baseSettings.CONFESSION_CHECK_TIMER)
async def resetUnreviewedConfessions(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    StaticMethods.resetUnfinishedConfessions()
    db = Database()
    value = db.getAllUnreviewedConfessions()
    if value:
        minVal = 99
        minAlertsId = 0
        for val in value:
            if val[0] not in globals.confessionIds:
                globals.confessionIds[val[0]] = 1
            if minVal > globals.confessionIds[val[0]]:
                minVal = globals.confessionIds[val[0]]
                minAlertsId = val[0]
        alertIntervals = baseSettings.CONFESSION_ALERT_INTERVALS
        minVal = len(alertIntervals)-1 if minVal > len(alertIntervals)-1 else minVal
        if StaticMethods.timeToSeconds(globals.confessionIds["alert"]) >= alertIntervals[minVal]:
            globals.confessionIds[minAlertsId] += 1
            await rest.create_message(channel=baseSettings.CONFESSTION_CHANNEL_ID, content=f"There are {len(value)} confessions in need of review =)\n Use </ymod confess-review:{baseSettings.CONFESS_REVIEW_COMMAND_ID}> to review them")
            globals.confessionIds["alert"] = time.time()
            for k, v in globals.confessionIds.items():
                if v < globals.confessionIds[minAlertsId]:
                    globals.confessionIds[k] = globals.confessionIds[minAlertsId]

@component.with_schedule
@tanjun.as_interval(baseSettings.APPEAL_CHECK_TIMER)
async def resetUnreviewedAppeals(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    StaticMethods.resetUnfinishedAppeals()
    db = Database()
    value = db.getAllUnreviewedAppeals()
    if value:
        minVal = 99
        minAlertsId = 0
        for val in value:
            if val[0] not in globals.appealIds:
                globals.appealIds[val[0]] = 1
            if minVal > globals.appealIds[val[0]]:
                minVal = globals.appealIds[val[0]]
                minAlertsId = val[0]
        alertIntervals = baseSettings.APPEAL_ALERT_INTERVALS
        minVal = len(alertIntervals)-1 if minVal > len(alertIntervals)-1 else minVal
        if StaticMethods.timeToSeconds(globals.appealIds["alert"]) >= alertIntervals[minVal]:
            globals.appealIds[minAlertsId] += 1
            await rest.create_message(channel=baseSettings.APPEAL_CHANNEL_ID, content=f"There are {len(value)} appeals in need of review =)\n Use </ymod appeal-review:{baseSettings.APPEAL_REVIEW_COMMAND_ID}> to review them")
            globals.appealIds["alert"] = time.time()
            for k, v in globals.appealIds.items():
                if v < globals.appealIds[minAlertsId]:
                    globals.appealIds[k] = globals.appealIds[minAlertsId]

app = FastAPI()
@component.with_schedule
@tanjun.as_interval(30, max_runs=1)
async def startWebhookServer(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if not baseSettings.webhookPort or not baseSettings.webhookHostIp: 
        return
    Kick.DeleteAllWebhooks() # Kick stops sending webhooks to a server that hasn't responded (down or restart). Deleting and resubbing fixes that
    app.state.restClient = rest
    await checkKick(rest)
    loop = asyncio.get_running_loop()
    config = uvicorn.Config("plugins.checks:app", port=baseSettings.webhookPort,host = baseSettings.webhookHostIp, log_level=baseSettings.OTHER_LIBRARIES_LOG_LEVEL)
    server = uvicorn.Server(config)
    logging.getLogger("uvicorn.access").addFilter(StaticMethods.EndpointFilter())
    loop.run_until_complete(await server.serve())

@app.post(baseSettings.webhookEndpoint)
async def receiveWebhook(request:Request, background_tasks: BackgroundTasks):
    payload = await request.body()
    headers = request.headers
    background_tasks.add_task(processWebhookData, payload.decode('utf-8'), headers)
    return {"status": "ok", "message": "Webhook received and is being processed."}

@app.get(baseSettings.healthEndpoint)
async def checkHealth():
    shortest, ndShortest = StaticMethods.GetShortestActiveCheckTimer()
    badHealthMultiplier = baseSettings.badHealthMultiplier
    badHealth = shortest * badHealthMultiplier
    ndBadHealth = ndShortest * badHealthMultiplier
    timeSinceLastCheck = time.time() - globals.lastCheckTime
    ndTimeSinceLastCheck = time.time() - globals.lastNoDriverCheckTime
    if badHealth < timeSinceLastCheck or ndBadHealth < ndTimeSinceLastCheck:
        statusCode  = 503
        message = "Too long since last check time. Bad Health"
        logger.critical(f"Failed health check. {timeSinceLastCheck} and {ndTimeSinceLastCheck} seconds since last online check")
    else:
        statusCode = 200
        message = "Sassbot running well"
        logger.debug(f"Health check Pass: LastCheck: {timeSinceLastCheck} LastCheckND: {ndTimeSinceLastCheck}")
    return JSONResponse(content={"message": f"{message}"}, status_code=statusCode)

@app.get(baseSettings.kickOathCallbackEndpoint)
async def OAuthCallback(code: str = None, state: str = None, error: str = None):
    if error:
        logger.debug("got callback error")
        raise HTTPException(
            status_code=401, 
            detail=f"Authorization failed. Error: {error}"
        )
    if not state or state not in globals.kickOauth:
        logger.debug("oauth state didn't match")
        raise HTTPException(
            status_code=403, 
            detail="State mismatch. Possible CSRF attack. Access denied."
        )
    try:
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        token_url = "https://id.kick.com/oauth/token" 
        discordId = globals.kickOauth[state][0]
        codeVerifier = globals.kickOauth[state][1]

        payload = {
            'code': code,
            'client_id': baseSettings.kickClientId,
            'client_secret': baseSettings.kickClientSecret,
            'redirect_uri': baseSettings.kickRedirectUrl, 
            'grant_type': 'authorization_code',
            'code_verifier': codeVerifier  
        }

        response = requests.post(token_url, data=payload, headers=headers)
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)

        del globals.kickOauth[state]
        token_data = response.json()
        accessToken = token_data['access_token']
        refreshToken = token_data["refresh_token"]
        tokenType = token_data["token_type"]
        accessToken = tokenType + " " + accessToken
        userResponse = Kick.GetUserInfoFromToken(accessToken)
        userResponse = userResponse.json()
        userId = userResponse['data'][0]['user_id']
        userName = userResponse['data'][0]['name']
        email = userResponse['data'][0]['email']
        #profilePicture = userResponse['data'][0]['profile_picture'] # behind verification? dumb
        db = Database()
        db.insertKickUser(userId,userName,refreshToken=refreshToken, email=email)
        db.insertDiscordKickAccountConnection(discordId, userId)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to exchange code for token: {e}")
    return RedirectResponse(url=baseSettings.kickDiscordRedirect)

async def processWebhookData(body, headers):
    if 'kick-event-type' not in headers or time.time() - globals.kickLastAlertWebhook < baseSettings.WAIT_BETWEEN_MESSAGES: 
        return
    globals.kickLastAlertWebhook = time.time()
    if Kick.verifyWebhook(headers, body):
        logger.debug("verified kick webhook")
        if headers['kick-event-type'] == "livestream.status.updated":
            body = json.loads(body)
            if body['is_live']:
                kickUserName = body['broadcaster']['channel_slug']
                globals.kickProfilePics[kickUserName.lower()] = body['broadcaster']['profile_picture']
            await checkKick(app.state.restClient)
    else:
        logger.warning("failed to verify incoming kick webhook")
            
    logger.debug(body)
    logger.debug(str(headers))

@component.with_schedule
@tanjun.as_interval(baseSettings.KICK_CHECK_TIMER)
async def checkKickClips(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    today = datetime.date.today()
    isoYear, isoWeek, isoDayOfWeek = today.isocalendar()
    yearWeek = f"{isoYear}:{isoWeek}"
    db = Database()
    exeString = f'''SELECT year_week FROM kick_clips_heroes WHERE year_week='{yearWeek}' '''
    for kickUserName in baseSettings.kickUserName:
        if not db.isExists(exeString):
            await KickDataGrabber.CollectClipData(kickUserName.lower(), rest)

@component.with_schedule
@tanjun.as_time_schedule(minutes=[0,10,20,30,40,50])
async def memberLogger(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    members = rest.fetch_members(baseSettings.GUILD_ID)
    db = Database()
    logger.debug("adding discord users to DB")
    async for member in members:
        db.insertDiscordUser(member.id, member.username)

@component.with_schedule
@tanjun.as_interval(30, max_runs=1)
async def startKickWebsocket(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if not baseSettings.kickChatroomId or not baseSettings.kickChannelId: 
        return
    lastLaunchTime = time.time()
    maxRetries = 3
    maxRetryWindow = 30
    numRetries = 0
    while numRetries <= maxRetries:
        await KickDataGrabber.connectKickWebSockets()
        logger.warning("Kick Websocket closed. Attempting to reconnect")
        timeSinceLastRetry = time.time() - lastLaunchTime
        if timeSinceLastRetry <= maxRetryWindow:
            numRetries += 1
        else:
            lastLaunchTime = time.time()
            numRetries = 1
    logger.critical("Kick Websocket failed after reaching max retries")

@component.with_schedule
@tanjun.as_interval(baseSettings.ROLE_ADD_REMOVE_TIMER)
async def AddKickRoles(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if not baseSettings.hasRolePermissions: 
        return
    db = Database()
    subsShortThreshold = baseSettings.kickSubsShortThreshold
    subsShortLookBackHours = baseSettings.kickSubsShortLookBackHours
    subsLongThreshold = baseSettings.kickSubsLongThreshold
    subsLongLookBackDays = baseSettings.kickSubsLongLookBackDays
    shortSubbers = db.GetSubTimeHours(subsShortLookBackHours, subsShortThreshold)
    longSubbers = db.GetSubTimeDays(subsLongLookBackDays,subsLongThreshold)
    try:
        await HandleShortSubRoles(rest, db, shortSubbers)
        await HandleLongSubRoles(rest, db, longSubbers)
    except hikari.errors.ForbiddenError:
        logger.warning("Don't have permission to change roles or own role isn't high enough")

async def HandleShortSubRoles(rest:hikari.impl.RESTClientImpl, db:Database, shortSubbers:dict):
    if not baseSettings.kickShortRoleId:
        logger.warning("kickShortRoleId has no value. Can't manage roles. Give it a role ID or set hasRolePermission to False")
        return
    for k,v in shortSubbers.items():
        discordId = db.GetDiscordKickConnection(k)
        if discordId:
            member = await rest.fetch_member(baseSettings.GUILD_ID, discordId)
            roleId = baseSettings.kickShortRoleId
            roles = member.get_roles()
            isExist = False
            for role in roles:
                if roleId == role.id:
                    isExist = True
            if not isExist and not db.isHasShortDate(k):
                logger.debug("adding short role")
                lastSubDate = db.GetLastSubDate(k)
                await member.add_role(roleId)
                db.InsertShortRoleDate(k, roledate=lastSubDate)

async def HandleLongSubRoles(rest:hikari.impl.RESTClientImpl, db:Database, longSubbers:dict):
    if not baseSettings.kickLongRoleId:
        logger.warning("kickLongRoleId has no value. Can't manage roles. Give it a role ID or set hasRolePermission to False")
        return
    for k,v in longSubbers.items():
        discordId = db.GetDiscordKickConnection(k)
        if discordId:
            try:
                member = await rest.fetch_member(baseSettings.GUILD_ID, discordId)
                roleId = baseSettings.kickLongRoleId
                roles = member.get_roles()
                isExist = False
                for role in roles:
                    if roleId == role.id:
                        isExist = True
                if not isExist and not db.isHasLongDate(k):
                    logger.debug("adding long role")
                    await member.add_role(roleId)
                    lastSubDate = db.GetLastSubDate(k)
                    db.InsertLongRoleDate(k, roledate=lastSubDate)
            except hikari.errors.NotFoundError:
                #logger.debug("Not can't give or check role. Member left server")
                pass

@component.with_schedule
@tanjun.as_interval(baseSettings.ROLE_ADD_REMOVE_TIMER)
async def RemoveKickRoles(rest: alluka.Injected[hikari.impl.RESTClientImpl]) -> None:
    if not baseSettings.hasRolePermissions:
        return
    db = Database()
    longDateRolePeriod = baseSettings.kickLongDateRolePeriod
    shortTimeRolePeriod = baseSettings.kickShortTimeRolePeriod
    async for member in rest.fetch_members(baseSettings.GUILD_ID):
        kickId = db.GetKickDiscordConnection(member.id)
        dummyKickId = member.id * -1
        if baseSettings.kickLongRoleId in member.role_ids:
            if kickId:
                await CheckRemoveLongRole(db, longDateRolePeriod, member, kickId)
            else: 
                db.insertKickUser(dummyKickId, member.username)
                await CheckRemoveLongRole(db, longDateRolePeriod, member, dummyKickId)
        if baseSettings.kickShortRoleId in member.role_ids:
            if kickId:
                await CheckRemoveShortRole(db, shortTimeRolePeriod, member, kickId)
            else:
                db.insertKickUser(dummyKickId, member.username)
                await CheckRemoveShortRole(db,  shortTimeRolePeriod, member, dummyKickId)

async def CheckRemoveLongRole(db:Database, longDateRolePeriod, member, kickId):
    longDate = db.GetLongDate(kickId)
    if longDate: 
        longDate = datetime.datetime.fromisoformat(longDate)
        threshhold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=longDateRolePeriod)
        if longDate < threshhold:
            logger.debug(f"{member.username} kick Long sub role expired. Removing")
            await member.remove_role(baseSettings.kickLongRoleId)
            db.InsertLongRoleDate(kickId,roledate=None)
    else:
        db.InsertLongRoleDate(kickId)

async def CheckRemoveShortRole(db:Database, shortDateRolePeriod, member, kickId):
    shortDate = db.GetShortDate(kickId)
    if shortDate: 
        shortDate = datetime.datetime.fromisoformat(shortDate)
        threshhold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=shortDateRolePeriod)
        if shortDate < threshhold:
            logger.debug(f"{member.username} kick Short sub role expired. Removing")
            await member.remove_role(baseSettings.kickShortRoleId)
            db.InsertLongRoleDate(kickId,roledate=None)
    else:
        db.InsertShortRoleDate(kickId)