import asyncio
from EmbedCreator import EmbedCreator
from Constants import Constants
from Database import Database
import time
import hikari

class Notifications:
    async def OFNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, ofUserName):
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
        db.updatePlatformRowCol("platforms","onlyfans","last_online_message",time.time())
        IS_PING = db.getPing()
        messageContent = Constants.OF_ROLES_TO_PING + ofOnlineText if IS_PING else ofOnlineText
        await rest.create_message(channel = Constants.OF_NOTIFICATION_CHANNEL_ID, content = messageContent, embed = ofEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def ChaturNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, cbUserName):
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
                                    largeThumbnail= largeThumbnail, 
                                    useTwitter=False
                                )
        task = asyncio.create_task(embedMaker.getEmbed())
        cbEmbed = await task
        db = Database()
        db.updatePlatformRowCol("platforms","chaturbate","last_online_message",time.time())
        IS_PING = db.getPing()
        messageContent = Constants.CB_ROLES_TO_PING + cbOnlineText if IS_PING else cbOnlineText
        await rest.create_message(channel = Constants.CB_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=cbEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def FansNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, fansUserName):
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
        db.updatePlatformRowCol("platforms","fansly","last_online_message",time.time())
        IS_PING = db.getPing()
        messageContent = Constants.FANS_ROLES_TO_PING + fansOnlineText if IS_PING else fansOnlineText
        await rest.create_message(channel = Constants.FANS_NOTIFICATION_CHANNEL_ID, content = messageContent, embed = fansEmbed, mentions_everyone=IS_PING, role_mentions=IS_PING)

    async def TwitchNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, twitchUserName):
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
        db.updatePlatformRowCol("platforms","twitch","last_online_message",time.time())
        IS_PING = db.getPing()
        messageContent = Constants.TWITCH_ROLES_TO_PING + twitchOnlineText if IS_PING else twitchOnlineText
        await rest.create_message(channel = Constants.TWITCH_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=twitchEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)
    
    async def YTNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, ytUserName):
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
        db.updatePlatformRowCol("platforms","youtube","last_online_message",time.time())
        IS_PING = db.getPing()
        messageContent = Constants.YT_ROLES_TO_PING + ytOnlineText if IS_PING else ytOnlineText
        await rest.create_message(channel = Constants.YT_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=ytEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)
    
    async def KickNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, kickUserName):
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
        db.updatePlatformRowCol("platforms","kick","last_online_message",time.time())
        IS_PING = db.getPing()
        messageContent = Constants.KICK_ROLES_TO_PING + kickOnlineText if IS_PING else kickOnlineText
        await rest.create_message(channel = Constants.KICK_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=kickEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def Cam4Notification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, cam4UserName):
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
        db.updatePlatformRowCol("platforms","cam4","last_online_message",time.time())
        IS_PING = db.getPing()
        messageContent = Constants.CAM4_ROLES_TO_PING + cam4OnlineText if IS_PING else cam4OnlineText
        await rest.create_message(channel = Constants.CAM4_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=cam4Embed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def MfcNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, mfcUserName):
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
        db.updatePlatformRowCol("platforms","mfc","last_online_message",time.time())
        IS_PING = db.getPing()  
        messageContent = Constants.MFC_ROLES_TO_PING + mfcOnlineText if IS_PING else mfcOnlineText
        await rest.create_message(channel = Constants.MFC_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=mfcEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def BcNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, bcUserName):
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
        db.updatePlatformRowCol("platforms","bongacams","last_online_message",time.time())
        IS_PING = db.getPing()  
        messageContent = Constants.BC_ROLES_TO_PING + bcOnlineText if IS_PING else bcOnlineText
        await rest.create_message(channel = Constants.BC_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=bcEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)

    async def ScNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, scUserName):
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
        db.updatePlatformRowCol("platforms","stripchat","last_online_message",time.time())
        IS_PING = db.getPing()  
        messageContent = Constants.SC_ROLES_TO_PING + scOnlineText if IS_PING else scOnlineText
        await rest.create_message(channel = Constants.SC_NOTIFICATION_CHANNEL_ID, content = messageContent, embed=scEmbed, mentions_everyone= IS_PING, role_mentions=IS_PING)