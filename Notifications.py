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
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = ofEmbed)

    async def ChaturNotification(rest: hikari.impl.RESTClientImpl, title):
        db = Database()
        db.updateTableRowCol("platforms","chaturbate","last_online_message",time.time())
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.chaturOnlineText)

    async def FansNotification(rest: hikari.impl.RESTClientImpl, title):
        embedMaker = EmbedCreator(Constants.streamerName + " is live on Fansly!", "Naughty Sleep Stream? =)", Constants.fansLiveStreamUrl, 'images/FansImage.png', Constants.fansEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        fansEmbed = await task
        db = Database()
        db.updateTableRowCol("platforms","fansly","last_online_message",time.time())
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = fansEmbed)

    async def TwitchNotification(rest: hikari.impl.RESTClientImpl, title):
        db = Database()
        db.updateTableRowCol("platforms","twitch","last_online_message",time.time())
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.twitchOnlineText)
    
    async def YTNotification(rest: hikari.impl.RESTClientImpl, title):
        db = Database()
        db.updateTableRowCol("platforms","youtube","last_online_message",time.time())
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.ytOnlineText)
    
    async def KickNotification(rest: hikari.impl.RESTClientImpl, title):
        embedMaker = EmbedCreator(Constants.streamerName + " is live on Kick!", title, Constants.casKickUrl, 'images/KickImage.png', Constants.kickEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        kickEmbed = await task
        db = Database()
        db.updateTableRowCol("platforms","kick","last_online_message",time.time())
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = kickEmbed)
    
    async def KittiesKickNotification(rest: hikari.impl.RESTClientImpl,title):
        db = Database()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.kittiesKickOnlineText)
        db.updateTableRowCol("platforms","kittiesKick","last_online_message",time.time())