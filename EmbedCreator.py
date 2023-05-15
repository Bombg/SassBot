import hikari
from Constants import Constants
from TwitterImageGrabber import TwitterImageGrabber
import asyncio

class EmbedCreator:
    def __init__(self,title,description,url,thumbnail,color) -> None:
        self.title = title
        self.description = description
        self.url = url
        self.thumbnail = thumbnail
        self.color = color

    async def getEmbed(self):
        twitImgGrab = TwitterImageGrabber()
        task = asyncio.create_task(twitImgGrab.getImage())
        twitImg = await task
        embed = (
            hikari.Embed(
            title = self.title ,
            description = self.description,
            url = self.url,
            color = self.color
            ).set_image(twitImg)
            .set_thumbnail(self.thumbnail)
        )
        return embed