import hikari
import TwitterImageGrabber
import asyncio
from Constants import Constants
import StaticMethods

class EmbedCreator:
    def __init__(self,title,description,url,thumbnail,color,largeThumbnail = "") -> None:
        self.title = title
        self.description = description
        self.url = url
        self.thumbnail = thumbnail
        self.color = color
        self.largeThumbnail = largeThumbnail

    async def getEmbed(self):
        pinUrl = StaticMethods.checkImagePin()
        if Constants.twitterUrl:
            embedImg = await asyncio.get_running_loop().run_in_executor(None,TwitterImageGrabber.getImage)
        if self.largeThumbnail and not pinUrl:
            embedImg = self.largeThumbnail
        else:
            embedImg = StaticMethods.getEmbedImage()

        embed = (
            hikari.Embed(
            title = self.title ,
            description = self.description,
            url = self.url,
            color = self.color
            ).set_image(embedImg)
            .set_thumbnail(self.thumbnail)
        )
        return embed