import asyncio
from EmbedCreator import EmbedCreator
from Constants import Constants
from Database import Database
import time
import hikari

class Notifications:
    async def OFNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, ofUserName):
        OfLiveStreamUrl = f"https://onlyfans.com/{ofUserName}/live"
        ofOnlineText = Constants.streamerName + " is live on Onlyfans!\n<" + OfLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.streamerName + " is now live on Onlyfans!", 
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
        db.updateTableRowCol("platforms","onlyfans","last_online_message",time.time())
        PING_EVERYONE = db.getPing()
        messageContent = "@everyone " + ofOnlineText if PING_EVERYONE else ofOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed = ofEmbed, mentions_everyone= PING_EVERYONE)

    async def ChaturNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, cbUserName):
        cbLiveStreamUrl = f"https://chaturbate.com/{cbUserName}/"
        cbOnlineText = Constants.streamerName + " is live on Chaturbate!\n<" + cbLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    f"{Constants.streamerName} is now live on Chaturbate!", 
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
        db.updateTableRowCol("platforms","chaturbate","last_online_message",time.time())
        PING_EVERYONE = db.getPing()
        messageContent = "@everyone " + cbOnlineText if PING_EVERYONE else cbOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed=cbEmbed, mentions_everyone= PING_EVERYONE)

    async def FansNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, fansUserName):
        fansLiveStreamUrl = f"https://fansly.com/live/{fansUserName}"
        fansOnlineText = Constants.streamerName + " is live on Fansly!\n<" + fansLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.streamerName + " is now live on Fansly!", 
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
        db.updateTableRowCol("platforms","fansly","last_online_message",time.time())
        PING_EVERYONE = db.getPing()
        messageContent = "@everyone " + fansOnlineText if PING_EVERYONE else fansOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed = fansEmbed, mentions_everyone=PING_EVERYONE)

    async def TwitchNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, twitchUserName):
        twitchLiveStreamUrl = f"https://www.twitch.tv/{twitchUserName}"
        twitchOnlineText = Constants.streamerName + " is live on Twitch!\n<" + twitchLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.streamerName + " is now live on Twitch!", 
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
        db.updateTableRowCol("platforms","twitch","last_online_message",time.time())
        PING_EVERYONE = db.getPing()
        messageContent = "@everyone " + twitchOnlineText if PING_EVERYONE else twitchOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed=twitchEmbed, mentions_everyone= PING_EVERYONE)
    
    async def YTNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, ytUserName):
        ytLiveStreamUrl = f"https://www.youtube.com/@{ytUserName}/live"
        ytOnlineText = Constants.streamerName + " is live on YouTube!\n<" + ytLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.streamerName + " is now live on YouTube!", 
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
        db.updateTableRowCol("platforms","youtube","last_online_message",time.time())
        PING_EVERYONE = db.getPing()
        messageContent = "@everyone " + ytOnlineText if PING_EVERYONE else ytOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed=ytEmbed, mentions_everyone= PING_EVERYONE)
    
    async def KickNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, kickUserName):
        kickLiveStreamUrl = f"https://kick.com/{kickUserName}"
        kickOnlineText = Constants.streamerName + " is live on Kick!\n<" + kickLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.streamerName + " is now live on Kick!", 
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
        db.updateTableRowCol("platforms","kick","last_online_message",time.time())
        PING_EVERYONE = db.getPing()
        messageContent = "@everyone " + kickOnlineText if PING_EVERYONE else kickOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed=kickEmbed, mentions_everyone= PING_EVERYONE)

    async def Cam4Notification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, cam4UserName):
        cam4LiveStreamUrl = f"https://www.cam4.com/{cam4UserName}"
        cam4OnlineText = Constants.streamerName + " is live on Cam4!\n<" + cam4LiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.streamerName + " is now live on Cam4!", 
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
        db.updateTableRowCol("platforms","cam4","last_online_message",time.time())
        PING_EVERYONE = db.getPing()
        messageContent = "@everyone " + cam4OnlineText if PING_EVERYONE else cam4OnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed=cam4Embed, mentions_everyone= PING_EVERYONE)

    async def MfcNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, mfcUserName):
        mfcLiveStreamUrl = f"https://www.myfreecams.com/#{mfcUserName}"
        mfcOnlineText = Constants.streamerName + " is live on MyFreeCams!\n<" + mfcLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.streamerName + " is now live on MyFreeCams!", 
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
        db.updateTableRowCol("platforms","mfc","last_online_message",time.time())
        PING_EVERYONE = db.getPing()  
        messageContent = "@everyone " + mfcOnlineText if PING_EVERYONE else mfcOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed=mfcEmbed, mentions_everyone= PING_EVERYONE)

    async def BcNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, bcUserName):
        bcLiveStreamUrl = f"https://bongacams.com/{bcUserName}"
        bcOnlineText = Constants.streamerName + " is live on BongaCams!\n<" + bcLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.streamerName + " is now live on BongaCams!", 
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
        db.updateTableRowCol("platforms","bongacams","last_online_message",time.time())
        PING_EVERYONE = db.getPing()  
        messageContent = "@everyone " + bcOnlineText if PING_EVERYONE else bcOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed=bcEmbed, mentions_everyone= PING_EVERYONE)

    async def ScNotification(rest: hikari.impl.RESTClientImpl, title, largeThumbnail, icon, scUserName):
        scLiveStreamUrl = f"https://stripchat.com/{scUserName}"
        scOnlineText = Constants.streamerName + " is live on StripChat!\n<" + scLiveStreamUrl + ">"
        embedMaker = EmbedCreator(
                                    Constants.streamerName + " is now live on StripChat!", 
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
        db.updateTableRowCol("platforms","stripchat","last_online_message",time.time())
        PING_EVERYONE = db.getPing()  
        messageContent = "@everyone " + scOnlineText if PING_EVERYONE else scOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed=scEmbed, mentions_everyone= PING_EVERYONE)