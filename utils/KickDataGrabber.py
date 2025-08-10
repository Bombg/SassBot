from DefaultConstants import Settings as Settings
import logging
import utils.NoDriverBrowserCreator as ndb
import globals
import asyncio
import json
from utils.Database import Database
import datetime
from datetime import datetime as dt
from datetime import timedelta
from datetime import timezone
import hikari
import websockets
from checkers import Kick as Kick

baseSettings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)
#https://kick.com/{kickSlug}/clips/{clipId} 
async def CollectClipData(kickSlug:str, rest: hikari.impl.RESTClientImpl) -> None:
    db = Database()
    try:
        apiUrl = GetApiCheckGlobals(db, kickSlug)
        results = Kick.GetIntApiJsonTls(apiUrl)
        if not results or 'clips' not in results:
            logger.warning("Couldn't retreive Kick clips: non 200 status, cloudflare bot detection?")
            return
        if 'nextCursor' in results:
            if globals.kickClipCursor in globals.kickVisitedCursors:
                logger.debug("browser out of order after page load")
                return
            globals.kickVisitedCursors.append(globals.kickClipCursor)
            globals.kickClipCursor = results['nextCursor']
            logger.debug(f"grabbing clip data from {apiUrl} and going again at cursor: {results['nextCursor']}")
        else:
            db.MarkClipsFullyScanned()
        for clip in results['clips']:
            exeString = f'''SELECT clip_id FROM kick_clips WHERE clip_id='{clip['id']}' '''
            creationDate = dt.strptime(clip['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
            timeDiff = dt.now(timezone.utc) - creationDate
            daysClipLookBack = baseSettings.kickClipDaysLookBack
            if not db.isExists(exeString):
                if timeDiff < timedelta(days=daysClipLookBack):
                    db.addTempKickClipToTable(clip['id'], clip['livestream_id'],clip['channel']['slug'], clip['creator']['slug'], clip['created_at'], clip['title'], clip['views'], clip['category']['slug'])
                else:
                    db.addKickClipToTable(clip['id'], clip['livestream_id'],clip['channel']['slug'], clip['creator']['slug'], clip['created_at'], clip['title'], clip['views'], clip['category']['slug'])
            elif timeDiff < timedelta(days=daysClipLookBack):
                db.addTempKickClipToTable(clip['id'], clip['livestream_id'],clip['channel']['slug'], clip['creator']['slug'], clip['created_at'], clip['title'], clip['views'], clip['category']['slug'])
            elif db.isClipsFullyScanned():
                globals.kickClipCursor = ""
        if not db.isClipsFullyScanned():
            db.InsertClipCursor(results['nextCursor'])
        if not globals.kickClipCursor:
            await AnnounceWinnersHandleData(kickSlug, rest, db) 
    except Exception as e:
        logger.exception(e)
        globals.browserOpen = False

def GetApiCheckGlobals(db: Database, kickSlug):
    apiUrl = f"https://kick.com/api/v2/channels/{kickSlug}/clips"
    if db.isClipRowCountZero():
        db.addKickClipToTable("greenLight",None,None,None,None,None,None,None)
    if not db.isClipsFullyScanned():
        globals.kickClipCursor = db.GetClipCursor()
    if globals.kickClipCursor:
        apiUrl = f"{apiUrl}?cursor={globals.kickClipCursor}"
    return apiUrl
    
async def GetClipResultsNd(db:Database, apiUrl):
    browser = await ndb.GetBrowser(proxy=baseSettings.KICK_PROXY)
    if globals.kickClipCursor in globals.kickVisitedCursors:
        logger.debug("browser out of order pre page load")
        return
    await asyncio.sleep(1*baseSettings.NODRIVER_WAIT_MULTIPLIER)
    page = await browser.get(apiUrl)
    await asyncio.sleep(1*baseSettings.NODRIVER_WAIT_MULTIPLIER)
    await page.save_screenshot("KickClipsScreenshot.jpg")
    content = await page.get_content()
    content = content.split('<body>')
    if len(content) < 2:
        logger.warning("error with clip checker. user is banned,wrong username supplied, or cloudflare bot detection")
    else:
        jsonText = content[1].split('</body></html>')
        results = json.loads(jsonText[0])
    await ndb.CloseNDBrowser(browser, page)
    return results

async def AnnounceWinnersHandleData(kickSlug: str, rest:hikari.impl.RESTClientImpl, db:Database):
    today = datetime.date.today()
    isoYear, isoWeek, isoDayOfWeek = today.isocalendar()
    mostViews, mostViewsTitle, mostViewsClipper, mostViewsClipId, mostViewedUser, userViews, mostClipper, numClips = db.CalculateWeeklyKickClipWinners()
    mostViewedClipUrl = f'https://kick.com/{kickSlug}/clips/{mostViewsClipId}'
    messageContent=f"# Kick Clip Stats For Week {isoWeek} Of {isoYear}:\n" \
                    f"### Most Viewed Clipper:\n" \
                    f"- ** {mostViewedUser.capitalize()} ** with ** {userViews} ** total views gained across all their clips\n"\
                    f"### Most Prolific Clipper:\n" \
                    f"- ** {mostClipper.capitalize()} ** with ** {numClips} ** clips\n"\
                    f"## Most Viewed Clip:\n" \
                    f"- ** {mostViewsTitle.capitalize()} **  with ** {mostViews} ** views gained\n" \
                    f"     - clipped by: ** {mostViewsClipper.capitalize()} ** \n"\
                    f"     - ** {mostViewedClipUrl} **"
    if userViews and mostViewedUser and mostClipper and numClips and mostViewsTitle and mostViewsClipId and baseSettings.KICK_CLIPS_ANNOUNCEMENT_CHANNEL:
        await rest.create_message(channel=baseSettings.KICK_CLIPS_ANNOUNCEMENT_CHANNEL, content=messageContent)
    else:
        logger.warning("Weekly Kick Clip Data announcement cancelled. Data gathering interrupted, no data, or announcement channel not set")
    db.createWeeklyKickClipsData(f"{isoYear}:{isoWeek}",mostViewsClipId, mostViewedUser, mostClipper)

async def connectKickWebSockets():
    COMMON_HEADERS = {
    'Origin': 'https://kick.com',
    'Cache-Control': 'no-cache',
    'Accept-Language': 'en-GB,en;q=0.9,af-ZA;q=0.8,af;q=0.7,en-US;q=0.6',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    }
    PUSHER_WS_URL = 'wss://ws-us2.pusher.com/app/32cbd69e4b950bf97679?protocol=7&client=js&version=8.4.0-rc2&flash=false'
    CHATROOM_CHANNEL = f'chatrooms.{baseSettings.kickChatroomId}.v2' #f'chatrooms.{ChatroomId}.v2'  # App\\Events\\ChatMessageEvent
    CHATROOMV_TWO_CHANNEL  = f'chatroom_{baseSettings.kickChatroomId}' # f'chatroom_{ChatroomlId}' GiftedSubscriptionsEvent RewardRedeemedEvent
    CHATROOM_DOT_ID = f'chatrooms.{baseSettings.kickChatroomId}' # App\\Events\\ChatMessageSentEvent but this is for gifted subs
    CHANNEL_CHANNEL = f'channel.{baseSettings.kickChannelId}'  # f'channel.{ChannelId}' App\\Events\\ChannelSubscriptionEvent, App\\Events\\LuckyUsersWhoGotGiftSubscriptionsEvent, App\\Events\\StreamerIsLive, App\\Events\\StopStreamBroadcast
    CHANNEL_CHANNEL_UNDER = f'channel_{baseSettings.kickChannelId}' #GiftsLeaderboardUpdated
    channels = [CHATROOM_CHANNEL, CHATROOMV_TWO_CHANNEL, CHATROOM_DOT_ID, CHANNEL_CHANNEL, CHANNEL_CHANNEL_UNDER]
    #{'event': 'pusher:error', 'data': {'code': 4200, 'message': 'Please reconnect immediately'}}
    db = Database()
    try:
        async with websockets.connect(PUSHER_WS_URL, extra_headers=COMMON_HEADERS) as ws:
            logger.debug("[KickWS] Connection opened.")
            async for message in ws:
                try:
                    data = json.loads(message)
                    if data['event'] == 'pusher:connection_established':
                        socketData = json.loads(data['data'])
                        socketId = socketData.get('socket_id')
                        logger.debug(f"[KickWS] Socket established with ID: {socketId}")
                        for channel in channels:
                            await subWsChannel(channel, ws)
                    elif data['event'] == 'pusher:error' and data['data']['code'] == 4200:
                        await ws.close()
                        logger.warning("Kick Websocket dropped")
                    elif data['event'] == 'App\\Events\\ChannelSubscriptionEvent':
                        await ParseChannelSubscriptionEvent(db,data)
                    elif data['event'] == 'App\\Events\\LuckyUsersWhoGotGiftSubscriptionsEvent':
                        ParseLuckyUsersWhoGotGiftSubscriptionsEvent(db,data)
                    elif data['event'] == 'GiftedSubscriptionsEvent':
                        ParseGiftedSubscriptionsEvent(db,data)
                    elif data['event'] == 'App\\Events\\ChatMessageEvent':
                        ParseChatMessageEvent(db, data)
                    elif data['event'] == 'App\\Events\\ChatMessageSentEvent':
                        ParseChatMessageSentEvent(db, data)
                    elif data['event'] == 'App\\Events\\ChatMoveToSupportedChannelEvent':
                        #{'event': 'App\\Events\\ChatMoveToSupportedChannelEvent', 'data': '{"channel":{"id":1228709,"user_id":1270821,"slug":"litneyspears","is_banned":false,"playback_url":"https:\\/\\/fa723fc1b171.us-west-2.playback.live-video.net\\/api\\/video\\/v1\\/us-west-2.196233775518.channel.JlhOxRLIUFVC.m3u8","name_updated_at":null,"vod_enabled":true,"subscription_enabled":true,"is_affiliate":false,"can_host":false,"current_livestream":{"id":64667668,"slug":"71862049-gooners-wya-s-of","channel_id":1228709,"created_at":"2025-07-17 01:53:20","session_title":"GOONERS WYA \\ud83d\\udca6 | !S !OF \\ud83e\\udd0d","is_live":true,"risk_level_id":null,"start_time":"2025-07-17 01:53:20","source":null,"twitch_channel":null,"duration":0,"language":"English","is_mature":true,"viewer_count":402}},"slug":"vixie_vu","hosted":{"id":28325733,"username":"Vixie_Vu","slug":"vixie_vu","viewers_count":509,"is_live":true,"profile_pic":"https:\\/\\/files.kick.com\\/images\\/user\\/29361330\\/profile_image\\/conversion\\/86561101-7be7-4965-a7f1-fbad30e0f9b0-thumb.webp","category":"Pools, Hot Tubs & Bikinis","preview_thumbnail":{"srcset":"https:\\/\\/images.kick.com\\/video_thumbnails\\/WxdYFz9j5g7T\\/1jtGo55IcOLw\\/1080.webp?versionId=My0VMft2lsRuOWzVjVgnXXVr43d7i23N 1920w, https:\\/\\/images.kick.com\\/video_thumbnails\\/WxdYFz9j5g7T\\/1jtGo55IcOLw\\/720.webp?versionId=3EQJQWYA6OYTUQ6KDGl8rYtlFnX8zuNy 1280w, https:\\/\\/images.kick.com\\/video_thumbnails\\/WxdYFz9j5g7T\\/1jtGo55IcOLw\\/360.webp?versionId=1vFHo6TbDV2FW6Y93ljJpIlMDuu_8oUz 480w, https:\\/\\/images.kick.com\\/video_thumbnails\\/WxdYFz9j5g7T\\/1jtGo55IcOLw\\/160.webp?versionId=k56DvCY.TdvKrkKTCIurz.TwXorUqmIW 284w, https:\\/\\/images.kick.com\\/video_thumbnails\\/WxdYFz9j5g7T\\/1jtGo55IcOLw\\/480.webp?versionId=4sa4HO2r70fidHDvWT5PRQ_YviffS1Wj 640w","src":"https:\\/\\/images.kick.com\\/video_thumbnails\\/WxdYFz9j5g7T\\/1jtGo55IcOLw\\/720.webp?versionId=3EQJQWYA6OYTUQ6KDGl8rYtlFnX8zuNy"}}}', 'channel': 'channel.1228709'}
                        data = json.loads(data['data'])
                        hostedId = data['hosted']['id']
                        hostedUserName = data['hosted']['username']
                        logger.debug(f"{hostedUserName}:{hostedId} was hosted")
                    elif data['event'] == 'RewardRedeemedEvent':
                        #{'event': 'RewardRedeemedEvent', 'data': '{"reward_title":"da bears","user_id":1502053,"channel_id":20309633,"username":"Bombg","user_input":"","reward_background_color":"#1475E1"}', 'channel': 'chatroom_20041545'}
                        data = json.loads(data['data'])
                        redeemed = data['reward_title']
                        redeemInput = data['user_input']
                        redeemerId = data['user_id']
                        redeemerUserName = data['username']
                        logger.debug(f"{redeemerUserName}:{redeemerId} redeemed {redeemed}")
                    elif data['event'] == 'App\\Events\\UserBannedEvent':
                        #{'event': 'App\\Events\\UserBannedEvent', 'data': '{"id":"286ae0b2-bba8-497d-a783-1adf703cbe03","user":{"id":63349022,"username":"darer123","slug":"darer123"},"banned_by":{"id":0,"username":"Vixie_Vu","slug":"vixie_vu"},"permanent":false,"duration":1,"expires_at":"2025-07-18T08:12:14+00:00"}', 'channel': 'chatrooms.28037413.v2'}
                        data = json.loads(data['data'])
                        bannedUser = data['user']['username']
                        bannedUserId = data['user']['id']
                        bannerUser = data['banned_by']['username']
                        bannerUserId = data['banned_by']['id']
                        logger.debug(f"{bannedUser}:{bannedUserId} banned/timeout by: {bannerUser}:{bannerUserId}")
                    elif data['event'] == 'App\\Events\\SubscriptionEvent':
                        ParseSubscriptionEvent(db, data)
                    elif data['event'] == 'GiftsLeaderboardUpdated':
                        #{"event":"GiftsLeaderboardUpdated","data":"{\"leaderboard\":[{\"user_id\":3315987,\"username\":\"TH3_ST4B_H4PPY\",\"quantity\":2469},{\"user_id\":4984014,\"username\":\"Andygreenwood2014\",\"quantity\":2312},{\"user_id\":538703,\"username\":\"GamerGabe\",\"quantity\":806},{\"user_id\":960630,\"username\":\"edubz5184\",\"quantity\":514},{\"user_id\":35809627,\"username\":\"LaskaTheDanishViking\",\"quantity\":416},{\"user_id\":43644314,\"username\":\"peque5040\",\"quantity\":390},{\"user_id\":26634199,\"username\":\"StrawHat85\",\"quantity\":312},{\"user_id\":38875468,\"username\":\"Psycilocibin\",\"quantity\":290},{\"user_id\":49795136,\"username\":\"Ridindirty001\",\"quantity\":252},{\"user_id\":45092496,\"username\":\"kingblackshaft\",\"quantity\":250}],\"weekly_leaderboard\":[{\"user_id\":8348691,\"username\":\"allehej\",\"quantity\":40},{\"user_id\":3315987,\"username\":\"TH3_ST4B_H4PPY\",\"quantity\":25},{\"user_id\":32793864,\"username\":\"Gator6989\",\"quantity\":5},{\"user_id\":45092496,\"username\":\"kingblackshaft\",\"quantity\":5},{\"user_id\":4984014,\"username\":\"Andygreenwood2014\",\"quantity\":5},{\"user_id\":3450843,\"username\":\"Lukeus\",\"quantity\":2},{\"user_id\":1903856,\"username\":\"the_fire_tiger\",\"quantity\":2},{\"user_id\":69907818,\"username\":\"R1ckyBoo\",\"quantity\":1}],\"monthly_leaderboard\":[{\"user_id\":3315987,\"username\":\"TH3_ST4B_H4PPY\",\"quantity\":277},{\"user_id\":4984014,\"username\":\"Andygreenwood2014\",\"quantity\":182},{\"user_id\":43644314,\"username\":\"peque5040\",\"quantity\":115},{\"user_id\":45092496,\"username\":\"kingblackshaft\",\"quantity\":113},{\"user_id\":538703,\"username\":\"GamerGabe\",\"quantity\":50},{\"user_id\":63805513,\"username\":\"CrispRat\",\"quantity\":48},{\"user_id\":8348691,\"username\":\"allehej\",\"quantity\":46},{\"user_id\":960630,\"username\":\"edubz5184\",\"quantity\":40},{\"user_id\":1848562,\"username\":\"hitemup1234\",\"quantity\":20},{\"user_id\":3450843,\"username\":\"Lukeus\",\"quantity\":12}],\"gifter_id\":69907818,\"gifter_username\":\"R1ckyBoo\",\"gifted_quantity\":1}","channel":"channel_1143439"}
                        pass
                    else:
                        logger.debug(f"TODO: {data}")
                        # saneEvent = data['event'].replace("\\", "-")
                        # f = open(f"PusherExamples/{saneEvent}.txt", 'a')
                        # f.write(message + "\n")
                        # f.close()
                except json.JSONDecodeError:
                    logger.debug(f"Received non-JSON message: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        logger.exception(f"Connection closed. Code: {e.code}, Reason: {e.reason}")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")

def ParseSubscriptionEvent(db:Database, data):
    #{"event":"App\\Events\\SubscriptionEvent","data":"{\"chatroom_id\":31047538,\"username\":\"The_D0ctor\",\"months\":1}","channel":"chatrooms.31047538.v2"}
    channel = data['channel']
    data = json.loads(data['data'])
    userName = data['username']
    months = data['months']
    info = Kick.getChannelInfoResponse([userName]).json()
    userId = info['data'][0]['broadcaster_user_id']
    gifterUString = CreateGiftedUString(["self"],userName,1)
    if not isGiftedAlreadyExist(gifterUString):
        logger.debug(f"Inserting:SubscriptionEvent:{gifterUString}")
        HandleKickSub(db, userId, userName, 1, channel, months, gifterUString)

def HandleKickSub(db:Database, userId, userName, numGifted, channel,  months, gifterUString):
    currentDate = datetime.datetime.now(datetime.timezone.utc)
    db.insertKickSub(userId, userName, numGifted, currentDate.isoformat(), channel, selfSub=months)
    globals.kickGiftUStrings.append(gifterUString)


def ParseChatMessageEvent(db:Database, data):
    #3 types - message, reply, celebration
    #{'event': 'App\\Events\\ChatMessageEvent', 'data': '{"id":"bbcdbcfd-8619-40c2-a0d0-ae7cf4c7a932","chatroom_id":1221707,"content":"[emote:3989851:litneyspears4Max]on my way to show you love","type":"message","created_at":"2025-07-17T08:44:56+00:00","sender":{"id":3528468,"username":"OhLookItsMax","slug":"ohlookitsmax","identity":{"color":"#FF9D00","badges":[{"type":"vip","text":"VIP"},{"type":"subscriber","text":"Subscriber","count":26}]}},"metadata":{"message_ref":"1752741896375"}}', 'channel': 'chatrooms.1221707.v2'}
    #{"event":"App\\Events\\ChatMessageEvent","data":"{\"id\":\"37e2ddbd-302c-4e5a-beda-4913c1747459\",\"chatroom_id\":1221707,\"content\":\"this is what someone deals with after Litney goes through Deadspace\",\"type\":\"reply\",\"created_at\":\"2025-07-19T03:47:45+00:00\",\"sender\":{\"id\":3528468,\"username\":\"OhLookItsMax\",\"slug\":\"ohlookitsmax\",\"identity\":{\"color\":\"#FF9D00\",\"badges\":[{\"type\":\"vip\",\"text\":\"VIP\"},{\"type\":\"subscriber\",\"text\":\"Subscriber\",\"count\":26}]}},\"metadata\":{\"original_sender\":{\"id\":2853400,\"username\":\"justdavid787\"},\"original_message\":{\"id\":\"91c93aae-23c4-4f62-acae-a3ca5782b8c7\",\"content\":\"this is like DeadSpace but weirder [emote:37225:KEKLEO]\"},\"message_ref\":\"1752896864929\"}}","channel":"chatrooms.1221707.v2"}
    #{"event":"App\\Events\\ChatMessageEvent","data":"{\"id\":\"1fc36aef-d1c8-4af3-841f-0d38574b73c3\",\"chatroom_id\":31047538,\"content\":\"\\ud83c\\udf89\",\"type\":\"celebration\",\"created_at\":\"2025-07-19T14:18:32+00:00\",\"sender\":{\"id\":11497484,\"username\":\"jerkpupputo\",\"slug\":\"jerkpupputo\",\"identity\":{\"color\":\"#FF9D00\",\"badges\":[{\"type\":\"founder\",\"text\":\"Founder\"},{\"type\":\"subscriber\",\"text\":\"Subscriber\",\"count\":2}]}},\"metadata\":{\"celebration\":{\"id\":\"chceleb_01K0518CW5PNSCAWDSXZY5806C\",\"type\":\"subscription_renewed\",\"total_months\":2,\"created_at\":\"2025-07-14T17:55:52.83787Z\"}}}","channel":"chatrooms.31047538.v2"}
    channel = data['channel']
    data = json.loads(data['data'])
    message = data['content']
    userId = data['sender']['id']
    userName = data['sender']['username']
    #collect emote data . Message data?
    db.insertKickUser(userId, userName)
    if data['type'] == 'celebration' and data['metadata']['celebration']['type'] == 'subscription_renewed' :
        months = data['metadata']['celebration']['total_months']
        giftedUstring = CreateGiftedUString(["self"],userName,1)
        if not isGiftedAlreadyExist(giftedUstring):
            logger.debug(f"Inserting: {giftedUstring}")
            HandleKickSub(db, userId, userName, 1, channel, months, giftedUstring)
    elif data['type'] == 'celebration':
        logger.debug(f"TODO: {data}")
    elif data['type'] != "celebration" and data['type'] != "reply" and data['type'] != "message":
        logger.debug(f"TODO:{data}")
    elif data['type'] =='message':
        identity = data['sender']['identity']
        db.InsertKickChatToTable(userId, userName, message, json.dumps(identity),data['created_at'],None,channel)
    elif data['type'] =='reply':
        identity = data['sender']['identity']
        repliedTo = data['metadata']
        db.InsertKickChatToTable(userId, userName, message, json.dumps(identity),data['created_at'],json.dumps(repliedTo),channel)

def ParseLuckyUsersWhoGotGiftSubscriptionsEvent(db:Database, data):
    #{'event': 'App\\Events\\LuckyUsersWhoGotGiftSubscriptionsEvent', 'data': '{"channel":{"id":17425723,"user_id":18312333,"slug":"nelkboys","is_banned":false,"playback_url":"https:\\/\\/fa723fc1b171.us-west-2.playback.live-video.net\\/api\\/video\\/v1\\/us-west-2.196233775518.channel.ze6nVEIVJ53v.m3u8","name_updated_at":null,"vod_enabled":true,"subscription_enabled":true,"is_affiliate":true,"can_host":true,"chatroom":{"id":17172694,"chatable_type":"App\\\\Models\\\\Channel","channel_id":17425723,"created_at":"2023-08-25T17:13:46.000000Z","updated_at":"2025-07-02T17:19:50.000000Z","chat_mode_old":"public","chat_mode":"public","slow_mode":true,"chatable_id":17425723,"followers_mode":true,"subscribers_mode":false,"emotes_mode":false,"message_interval":5,"following_min_duration":180}},"usernames":["kernanator","OhDollar","UZJ100","slimetimelive","m1nt710","k8dot","ginja47ninja","jbizzle007","MEATTIP","Danni2g","big_fat_black_testicles","DIZOTIZY","ck_certified","fletchyflipem","tturtlees","NickelinDime","ZACHROCK9","duey_17","1stScoop","PurpleArmyCX","Yettipnw","Jackyboy13","Beau4","nickv4","Iceman299","Dats_Lvke","Walidq695","chamoney2","Kushaug","Charredd","Cherts","ckmitch","Mattsark","Bee_Lu","Cman12","Scarcerow","EyezChico","Pizza_farts","BurgerGrease","BigCabbyDaddy","Chess_zebra","Denver7","BS3VEN","KyleRousseau38","KyleMay","HoonieStonebag","Kongwtf","brianc12","MyManTitsSlap","dkny25"],"gifter_username":"astra555"}', 'channel': 'channel.17425723'}
    data = json.loads(data['data'])
    userName = data['gifter_username']
    giftList = data['usernames']
    numGifted = len(giftList)
    logger.debug(f"LuckyUsersWhoGotGiftSubscriptionsEvent: Check for insertions or handle")

async def ParseChannelSubscriptionEvent(db:Database, data):
    #{"event":"App\\Events\\ChannelSubscriptionEvent","data":"{\"user_ids\":[62315363,2872386,3225896,59025745,2398519,2086888,2086799],\"username\":\"\",\"channel_id\":31335859}","channel":"channel.31335859"}
    #{'event': 'App\\Events\\ChannelSubscriptionEvent', 'data': '{"user_ids":[67477867],"username":"noahwjbrennan","channel_id":17425723}', 'channel': 'channel.17425723'}
    data = json.loads(data['data'])
    userId = data['user_ids'][0] 
    userName = data['username'] # if userName is null perhaps they got gifted and not self sub
    if userName:
        giftedUstring = CreateGiftedUString(["self"],userName,1)
        await asyncio.sleep(5)
        if not isGiftedAlreadyExist(giftedUstring):
            logger.debug(f"ChannelSubscriptionEvent:CHECK:{giftedUstring} Inserted or not")
    else:
        logger.debug(f"ChannelSubscriptionEvent(gifted version): insertion? may be reserved for anon gifts?")
        logger.debug(data)

def ParseGiftedSubscriptionsEvent(db:Database, data):
    #{'event': 'GiftedSubscriptionsEvent', 'data': '{"chatroom_id":25951243,"gifted_usernames":["rawze"],"gifter_username":"F1Aa","gifter_total":1}', 'channel': 'chatroom_25951243'}
    channel = data['channel']
    data = json.loads(data['data'])
    userName = data['gifter_username'] # Only event sometimes?
    totalGifted = data['gifter_total'] # num gifted overall in channel over time (200,300 etc)
    numGifted = len(data['gifted_usernames'])
    giftedList = data['gifted_usernames']
    giftedUString = CreateGiftedUString(giftedList, userName, numGifted)
    if not isGiftedAlreadyExist(giftedUString):
        logger.debug(f"Inserting: GiftedSubscriptionsEvent:{giftedUString}")
        info = Kick.getChannelInfoResponse([userName]).json()
        userId = info['data'][0]['broadcaster_user_id']
        HandleKickSub(db, userId, userName, numGifted, channel, None, giftedUString)

def ParseChatMessageSentEvent(db:Database, data):
    #{'event': 'App\\Events\\ChatMessageSentEvent', 'data': '{"message":{"id":"93ae8404-b077-46ba-a095-76f167b3b185","message":null,"type":"info","replied_to":null,"is_info":null,"link_preview":null,"chatroom_id":1221707,"role":"user","created_at":1751605454,"action":"gift","optional_message":null,"months_subscribed":null,"subscriptions_count":5,"giftedUsers":[{"username":"Terraflux","monthsSubscribed":1},{"username":"xHayir","monthsSubscribed":1},{"username":"Darren911","monthsSubscribed":1},{"username":"Hoodhotest","monthsSubscribed":1},{"username":"thetroublewithravens","monthsSubscribed":1}]},"user":{"id":2289061,"username":"PhatBoiLotto","role":"user","isSuperAdmin":null,"profile_thumb":"https:\\/\\/kick-files-prod.s3.us-west-2.amazonaws.com\\/images\\/user\\/2289061\\/profile_image\\/conversion\\/462cfe47-917a-46d7-8db4-f79a4dcae213-thumb.webp?X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAS3MDRZGPDOOAYROR%2F20250704%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250704T050415Z&X-Amz-SignedHeaders=host&X-Amz-Expires=299&X-Amz-Signature=4dbf64a8b9d3ad89c30bc8c4fac2c284800f98e26c7ef842fceec03d7969b2ba","verified":false,"follower_badges":[],"is_subscribed":null,"is_founder":false,"months_subscribed":null,"quantity_gifted":0}}', 'channel': 'chatrooms.1221707'}
    channel = data['channel']
    data = json.loads(data['data'])
    numGifted = data['message']['subscriptions_count'] # num gifted in the single event (1,5 10, 20 etc) 0 gifted is self sub
    userId = data['user']['id']
    userName = data['user']['username']
    if numGifted > 0:
        giftedList = MakeGiftedList(data['message']['giftedUsers'])
        giftedUString = CreateGiftedUString(giftedList, userName, numGifted)
        if not isGiftedAlreadyExist(giftedUString):
            logger.debug(f"Inserting:ChatMessageSentEvent:{giftedUString}")
            HandleKickSub(db, userId, userName, numGifted, channel, None, giftedUString)
    else:
        giftedUString = CreateGiftedUString(["self"], userName, 1)
        if not isGiftedAlreadyExist(giftedUString):
            logger.debug(f"Inserting:ChatMessageSentEvent:{giftedUString}")
            months = data['user']['months_subscribed']
            HandleKickSub(db, userId, userName, 1, channel, months, giftedUString)

async def subWsChannel(channel, ws):
    subscribeMessage = {
                            "event": "pusher:subscribe",
                            "data": {
                                "channel": channel
                            }
                        }
    await ws.send(json.dumps(subscribeMessage))
    logger.debug(f"[KickWS] Sent subscription request to channel: {channel}")

def isGiftedAlreadyExist(giftedUString):
    exists = False
    if giftedUString and giftedUString in globals.kickGiftUStrings:
        exists = True
    return exists

def CreateGiftedUString(giftedList:list, gifter:str, numGifted:int) -> str:
    # numGifted:Gifter:Giftee1:Giftee2... in alphabetical
    if not giftedList or not gifter or not numGifted: return ""
    giftedList.sort()
    giftedUString = f"{numGifted}:{gifter.lower()}"
    for giftee in giftedList:
        giftedUString = giftedUString + ":" + giftee.lower()
    return giftedUString

def MakeGiftedList(giftedUsers):
    giftedList = []
    for giftee in giftedUsers:
        giftedList.append(giftee['username'])
    return giftedList