import asyncio
from EmbedCreator import EmbedCreator
from Constants import Constants
import time
import globals

class Notifications:
    async def OFNotification(rest):
        embedMaker = EmbedCreator("Cass is live on Onlyfans!", "Naughty time? =)", Constants.OfLiveStreamUrl, 'images/OFImage.jpg', Constants.ofEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        ofEmbed = await task
        globals.onlyLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = ofEmbed)

    async def ChaturNotification(rest):
        globals.chaturLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.chaturOnlineText)

    async def FansNotification(rest):
        embedMaker = EmbedCreator("Cass is live on Fansly!", "Naughty Sleep Stream? =)", Constants.fansLiveStreamUrl, 'images/FansImage.png', Constants.fansEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        fansEmbed = await task
        globals.fansLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = fansEmbed)

    async def TwitchNotification(rest):
        globals.twitchLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.twitchOnlineText)
    
    async def YTNotification(rest):
        globals.ytLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.ytOnlineText)
    
    async def KickNotification(rest, title):
        embedMaker = EmbedCreator("Cass is live on Kick!", title, Constants.casKickUrl, 'images/KickImage.png', Constants.kickEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        kickEmbed = await task
        globals.kickLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = kickEmbed)