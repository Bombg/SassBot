import hikari
import asyncio
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
import utils.StaticMethods as StaticMethods

class EmbedCreator:
    def __init__(self,description,title,url,thumbnail,color,icon,username,largeThumbnail = "") -> None:
        self.title = title
        self.description = description
        self.url = url
        self.thumbnail = thumbnail
        self.color = color
        self.largeThumbnail = largeThumbnail
        self.icon = icon
        self.username = username

    async def getEmbed(self):
        thumbnailImage = await self.getThumbnailImage()
        embed = (
            hikari.Embed(
            title = self.title ,
            description = self.description,
            url = self.url,
            color = self.color
            ).set_image(thumbnailImage)
            .set_thumbnail(self.thumbnail)
            .set_author(name = self.username, url = self.url, icon = self.icon)
        )
        return embed

    async def getThumbnailImage(self):
        pinUrl = StaticMethods.checkImagePin()
        if self.largeThumbnail and not pinUrl:
            embedImg = self.largeThumbnail
        else:
            embedImg = StaticMethods.getEmbedImage()
        return embedImg