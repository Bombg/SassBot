import asyncio
from EmbedCreator import EmbedCreator
from Constants import Constants
import time
import globals

class Notifications:
    async def OFNotification(rest):
        embedMaker = EmbedCreator("Cass is live on Onlyfans!", "Naughty time? =)", Constants.casOnlyUrl, 'images/OFImage.jpg', Constants.ofEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        ofEmbed = await task
        globals.onlyFalse = 0
        globals.onlyLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = ofEmbed)

    async def ChaturNotification(rest):
        globals.chaturFalse = 0
        globals.chaturLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.chaturOnlineText)

    async def FansNotification(rest):
        embedMaker = EmbedCreator("Cass is live on Fansly!", "Naughty Sleep Stream? =)", Constants.casFansUrl, 'images/FansImage.png', Constants.fansEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        fansEmbed = await task
        globals.fansFalse = 0
        globals.fansLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = fansEmbed)

    async def TwitchNotification(rest):
        globals.twitchFalse = 0
        globals.twitchLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.twitchOnlineText)
    
    async def YTNotification(rest):
        globals.ytFalse = 0
        globals.ytLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = Constants.ytOnlineText)
    
    async def KickNotification(rest, title):
        embedMaker = EmbedCreator("Cass is live on Kick!", title, Constants.casKickUrl, 'images/KickImage.png', Constants.kickEmbedColor)
        task = asyncio.create_task(embedMaker.getEmbed())
        kickEmbed = await task
        globals.kickFalse = 0
        globals.kickLastOnlineMessage = time.time()
        await rest.create_message(channel = Constants.STDOUT_CHANNEL_ID, content = kickEmbed)