import hikari
import TwitterImageGrabber
import asyncio
from Constants import Constants
import StaticMethods

class EmbedCreator:
    def __init__(self,title,description,url,thumbnail,color) -> None:
        self.title = title
        self.description = description
        self.url = url
        self.thumbnail = thumbnail
        self.color = color

    async def getEmbed(self):
        if Constants.twitterUrl:
            embedImg = await asyncio.get_running_loop().run_in_executor(None,TwitterImageGrabber.getImage)
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