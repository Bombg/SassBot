import asyncio
from EmbedCreator import EmbedCreator
from Constants import Constants
from Database import Database
import time
import hikari

class Notifications:
    async def OFNotification(rest: hikari.impl.RESTClientImpl, title):
        embedMaker = EmbedCreator(Constants.streamerName + " is live on Onlyfans!", "Naughty time? =)", Constants.OfLiveStreamUrl, 'images/OFImage.jpg', Constants.ofEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        ofEmbed = await task
        db = Database()
        db.updateTableRowCol("platforms","onlyfans","last_online_message",time.time())
        messageContent = "@everyone " + Constants.ofOnlineText if Constants.PING_EVERYONE else Constants.ofOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed = ofEmbed, mentions_everyone= Constants.PING_EVERYONE)

    async def ChaturNotification(rest: hikari.impl.RESTClientImpl, title):
        db = Database()
        db.updateTableRowCol("platforms","chaturbate","last_online_message",time.time())
        messageContent = "@everyone " + Constants.chaturOnlineText if Constants.PING_EVERYONE else Constants.chaturOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, mentions_everyone= Constants.PING_EVERYONE)

    async def FansNotification(rest: hikari.impl.RESTClientImpl, title):
        embedMaker = EmbedCreator(Constants.streamerName + " is live on Fansly!", "Naughty Sleep Stream? =)", Constants.fansLiveStreamUrl, 'images/FansImage.png', Constants.fansEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        fansEmbed = await task
        db = Database()
        db.updateTableRowCol("platforms","fansly","last_online_message",time.time())
        messageContent = "@everyone " + Constants.fansOnlineText if Constants.PING_EVERYONE else Constants.fansOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed = fansEmbed, mentions_everyone=Constants.PING_EVERYONE)

    async def TwitchNotification(rest: hikari.impl.RESTClientImpl, title):
        db = Database()
        db.updateTableRowCol("platforms","twitch","last_online_message",time.time())
        messageContent = "@everyone " + Constants.twitchOnlineText if Constants.PING_EVERYONE else Constants.twitchOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent,mentions_everyone= Constants.PING_EVERYONE)
    
    async def YTNotification(rest: hikari.impl.RESTClientImpl, title):
        db = Database()
        db.updateTableRowCol("platforms","youtube","last_online_message",time.time())
        messageContent = "@everyone " + Constants.ytOnlineText if Constants.PING_EVERYONE else Constants.ytOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, mentions_everyone= Constants.PING_EVERYONE)
    
    async def KickNotification(rest: hikari.impl.RESTClientImpl, title):
        embedMaker = EmbedCreator(Constants.streamerName + " is live on Kick!", title, Constants.casKickUrl, 'images/KickImage.png', Constants.kickEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        kickEmbed = await task
        db = Database()
        db.updateTableRowCol("platforms","kick","last_online_message",time.time())
        messageContent = "@everyone " + Constants.kickOnlineText if Constants.PING_EVERYONE else Constants.kickOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, embed=kickEmbed, mentions_everyone= Constants.PING_EVERYONE)
    
    async def KittiesKickNotification(rest: hikari.impl.RESTClientImpl,title):
        db = Database()
        messageContent = "@everyone " + Constants.kittiesKickOnlineText if Constants.PING_EVERYONE else Constants.kittiesKickOnlineText
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = messageContent, mentions_everyone= Constants.PING_EVERYONE)
        db.updateTableRowCol("platforms","kittiesKick","last_online_message",time.time())