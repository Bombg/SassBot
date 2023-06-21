import hikari
import TwitterImageGrabber
import asyncio
from Constants import Constants
import StaticMethods

class EmbedCreator:
    def __init__(self,description,title,url,thumbnail,color,icon,username,largeThumbnail = "",useTwitter = True) -> None:
        self.title = title
        self.description = description
        self.url = url
        self.thumbnail = thumbnail
        self.color = color
        self.largeThumbnail = largeThumbnail
        self.useTwitter = useTwitter
        self.icon = icon
        self.username = username

    async def getEmbed(self):
        pinUrl = StaticMethods.checkImagePin()
        if Constants.twitterUrl and self.useTwitter:
            embedImg = await asyncio.get_running_loop().run_in_executor(None,TwitterImageGrabber.getImage)
        if self.largeThumbnail and not pinUrl or not self.useTwitter and self.largeThumbnail:
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
            .set_author(name = self.username, url = self.url, icon = self.icon)
        )
        return embed