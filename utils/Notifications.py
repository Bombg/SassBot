import asyncio
from utils.EmbedCreator import EmbedCreator
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
from utils.Database import Database
import time
import hikari

class Notifications:
    async def OFNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, ofUserName, isRerun):
        OfLiveStreamUrl = f"https://onlyfans.com/{ofUserName}/live"
        ofOnlineText = Constants.ofAboveEmbedText +"\n<" + OfLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.ofBelowTitleText, 
                                    title, 
                                    OfLiveStreamUrl, 
                                    'images/platformImages/OFImage.png', 
                                    Constants.ofEmbedColor, 
                                    icon, 
                                    ofUserName
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        ofEmbed = await task
        db = Database()
        db.updatePlatformRowCol("onlyfans","last_online_message",time.time())
        db.updatePlatformAccountRowCol("onlyfans",ofUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.OF_RERUN_ROLES_TO_PING if isRerun else Constants.OF_ROLES_TO_PING
        messageContent = rolesToPing + ofOnlineText if IS_PING else ofOnlineText
        await rest.create_message(channel = Constants.OF_NOTIFICATION_CHANNEL_ID, content = messageContent, embed = ofEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def ChaturNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, cbUserName, isRerun):
        cbLiveStreamUrl = f"https://chaturbate.com/{cbUserName}/"
        cbOnlineText = Constants.cbAboveEmbedText + "\n<" + cbLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.cbBelowTitleText, 
                                    title, 
                                    cbLiveStreamUrl, 
                                    'images/platformImages/CbImage.png', 
                                    Constants.cbEmbedColor, 
                                    icon, 
                                    cbUserName, 
                                    largeThumbnail= largeThumbnail
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        cbEmbed = await task
        db = Database()
        db.updatePlatformRowCol("chaturbate","last_online_message",time.time())
        db.updatePlatformAccountRowCol("chaturbate",cbUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.CB_RERUN_ROLES_TO_PING if isRerun else Constants.CB_ROLES_TO_PING
        messageContent = rolesToPing + cbOnlineText if IS_PING else cbOnlineText
        await rest.create_message(channel = Constants.CB_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=cbEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def FansNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, fansUserName, isRerun):
        fansLiveStreamUrl = f"https://fansly.com/live/{fansUserName}"
        fansOnlineText = Constants.fansAboveEmbedText + "\n<" + fansLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.fansBelowTitleText, 
                                    title, 
                                    fansLiveStreamUrl, 
                                    'images/platformImages/FansImage.png', 
                                    Constants.fansEmbedColor, 
                                    icon, 
                                    fansUserName
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        fansEmbed = await task
        db = Database()
        db.updatePlatformRowCol("fansly","last_online_message",time.time())
        db.updatePlatformAccountRowCol("fansly",fansUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.FANS_RERUN_ROLES_TO_PING if isRerun else Constants.FANS_ROLES_TO_PING
        messageContent = rolesToPing + fansOnlineText if IS_PING else fansOnlineText
        await rest.create_message(channel = Constants.FANS_NOTIFICATION_CHANNEL_ID, content = messageContent, embed = fansEmbed, mentions_everyone=IS_PING, role_mentions=IS_PING)

    async def TwitchNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, twitchUserName, isRerun):
        twitchLiveStreamUrl = f"https://www.twitch.tv/{twitchUserName}"
        twitchOnlineText = Constants.twitchAboveEmbedText + "\n<" + twitchLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.twitchBelowTitleText, 
                                    title, 
                                    twitchLiveStreamUrl, 
                                    'images/platformImages/twitchImage.png', 
                                    Constants.twitchEmbedColor, 
                                    icon, 
                                    twitchUserName, 
                                    largeThumbnail= largeThumbnail
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        twitchEmbed = await task
        db = Database()
        db.updatePlatformRowCol("twitch","last_online_message",time.time())
        db.updatePlatformAccountRowCol("twitch",twitchUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.TWITCH_RERUN_ROLES_TO_PING if isRerun else Constants.TWITCH_ROLES_TO_PING
        messageContent = rolesToPing + twitchOnlineText if IS_PING else twitchOnlineText
        await rest.create_message(channel = Constants.TWITCH_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=twitchEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)
    
    async def YTNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, ytUserName, isRerun):
        ytLiveStreamUrl = f"https://www.youtube.com/@{ytUserName}/live"
        ytOnlineText = Constants.ytAboveEmbedText + "\n<" + ytLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.ytBelowTitleText, 
                                    title, 
                                    ytLiveStreamUrl, 
                                    'images/platformImages/ytImage.png', 
                                    Constants.ytEmbedColor, 
                                    icon, 
                                    ytUserName, 
                                    largeThumbnail= largeThumbnail
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        ytEmbed = await task
        db = Database()
        db.updatePlatformRowCol("youtube","last_online_message",time.time())
        db.updatePlatformAccountRowCol("youtube",ytUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.YT_RERUN_ROLES_TO_PING if isRerun else Constants.YT_ROLES_TO_PING
        messageContent = rolesToPing + ytOnlineText if IS_PING else ytOnlineText
        await rest.create_message(channel = Constants.YT_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=ytEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)
    
    async def KickNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, kickUserName, isRerun):
        kickLiveStreamUrl = f"https://kick.com/{kickUserName}"
        kickOnlineText = Constants.kickAboveEmbedText + "\n<" + kickLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.kickBelowTitleText, 
                                    title, 
                                    kickLiveStreamUrl, 
                                    'images/platformImages/KickImage.png', 
                                    Constants.kickEmbedColor, 
                                    icon, 
                                    kickUserName, 
                                    largeThumbnail= largeThumbnail
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        kickEmbed = await task
        db = Database()
        db.updatePlatformRowCol("kick","last_online_message",time.time())
        db.updatePlatformAccountRowCol("kick",kickUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.KICK_RERUN_ROLES_TO_PING if isRerun else Constants.KICK_ROLES_TO_PING
        messageContent = rolesToPing + kickOnlineText if IS_PING else kickOnlineText
        await rest.create_message(channel = Constants.KICK_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=kickEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def Cam4Notification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, cam4UserName, isRerun):
        cam4LiveStreamUrl = f"https://www.cam4.com/{cam4UserName}"
        cam4OnlineText = Constants.cam4AboveEmbedText + "\n<" + cam4LiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.cam4BelowTitleText, 
                                    title, 
                                    cam4LiveStreamUrl, 
                                    'images/platformImages/cam4Image.png', 
                                    Constants.cam4EmbedColor, 
                                    icon, 
                                    cam4UserName, 
                                    largeThumbnail= largeThumbnail
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        cam4Embed = await task
        db = Database()
        db.updatePlatformRowCol("cam4","last_online_message",time.time())
        db.updatePlatformAccountRowCol("cam4",cam4UserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.CAM4_RERUN_ROLES_TO_PING if isRerun else Constants.CAM4_ROLES_TO_PING
        messageContent = rolesToPing + cam4OnlineText if IS_PING else cam4OnlineText
        await rest.create_message(channel = Constants.CAM4_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=cam4Embed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def MfcNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, mfcUserName, isRerun):
        mfcLiveStreamUrl = f"https://www.myfreecams.com/#{mfcUserName}"
        mfcOnlineText = Constants.mfcAboveEmbedText + "\n<" + mfcLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.mfcBelowTitleText, 
                                    title, 
                                    mfcLiveStreamUrl, 
                                    'images/platformImages/mfcImage.png', 
                                    Constants.mfcEmbedColor, 
                                    icon, 
                                    mfcUserName, 
                                    largeThumbnail= largeThumbnail
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        mfcEmbed = await task
        db = Database()
        db.updatePlatformRowCol("mfc","last_online_message",time.time())
        db.updatePlatformAccountRowCol("mfc",mfcUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.MFC_RERUN_ROLES_TO_PING if isRerun else Constants.MFC_ROLES_TO_PING
        messageContent = rolesToPing + mfcOnlineText if IS_PING else mfcOnlineText
        await rest.create_message(channel = Constants.MFC_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=mfcEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def BcNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, bcUserName, isRerun):
        bcLiveStreamUrl = f"https://bongacams.com/{bcUserName}"
        bcOnlineText = Constants.bcAboveEmbedText + "\n<" + bcLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.bcBelowTitleText, 
                                    title, 
                                    bcLiveStreamUrl, 
                                    'images/platformImages/bcImage.png', 
                                    Constants.bcEmbedColor, 
                                    icon, 
                                    bcUserName, 
                                    largeThumbnail= largeThumbnail
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        bcEmbed = await task
        db = Database()
        db.updatePlatformRowCol("bongacams","last_online_message",time.time())
        db.updatePlatformAccountRowCol("bongacams",bcUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.BC_RERUN_ROLES_TO_PING if isRerun else Constants.BC_ROLES_TO_PING
        messageContent = rolesToPing + bcOnlineText if IS_PING else bcOnlineText
        await rest.create_message(channel = Constants.BC_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=bcEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def ScNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, scUserName, isRerun):
        scLiveStreamUrl = f"https://stripchat.com/{scUserName}"
        scOnlineText = Constants.scAboveEmbedText + "\n<" + scLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.scBelowTitleText, 
                                    title, 
                                    scLiveStreamUrl, 
                                    'images/platformImages/scImage.png', 
                                    Constants.scEmbedColor, 
                                    icon, 
                                    scUserName, 
                                    largeThumbnail= largeThumbnail
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        scEmbed = await task
        db = Database()
        db.updatePlatformRowCol("stripchat","last_online_message",time.time())
        db.updatePlatformAccountRowCol("stripchat",scUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.SC_RERUN_ROLES_TO_PING if isRerun else Constants.SC_ROLES_TO_PING
        messageContent = rolesToPing + scOnlineText if IS_PING else scOnlineText
        await rest.create_message(channel = Constants.SC_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=scEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def EpNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, epUserName, isRerun):
        epLiveStreamUrl = f"https://eplay.com/{epUserName}/live"
        epOnlineText = Constants.epAboveEmbedText + "\n<" + epLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.epBelowTitleText, 
                                    title, 
                                    epLiveStreamUrl, 
                                    'images/platformImages/epImage.png', 
                                    Constants.epEmbedColor, 
                                    icon, 
                                    epUserName, 
                                    largeThumbnail= largeThumbnail
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        epEmbed = await task
        db = Database()
        db.updatePlatformRowCol("eplay","last_online_message",time.time())
        db.updatePlatformAccountRowCol("eplay",epUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.EP_RERUN_ROLES_TO_PING if isRerun else Constants.EP_ROLES_TO_PING
        messageContent = rolesToPing + epOnlineText if IS_PING else epOnlineText
        await rest.create_message(channel = Constants.EP_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=epEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def MvNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, mvUserName, isRerun):
        mvLiveStreamUrl = f"https://www.manyvids.com/live/cam/{mvUserName}"
        mvOnlineText = Constants.mvAboveEmbedText + "\n<" + mvLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.mvBelowTitleText, 
                                    title, 
                                    mvLiveStreamUrl, 
                                    'images/platformImages/mvImage.png', 
                                    Constants.mvEmbedColor, 
                                    icon, 
                                    mvUserName, 
                                    largeThumbnail= largeThumbnail
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        mvEmbed = await task
        db = Database()
        db.updatePlatformRowCol("manyvids","last_online_message",time.time())
        db.updatePlatformAccountRowCol("manyvids",mvUserName,"last_online_message",time.time())
        IS_PING = db.getPing()
        rolesToPing = Constants.MV_RERUN_ROLES_TO_PING if isRerun else Constants.MV_ROLES_TO_PING
        messageContent = rolesToPing + mvOnlineText if IS_PING else mvOnlineText
        await rest.create_message(channel = Constants.MV_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=mvEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)