import hikari
import TwitterImageGrabber
import asyncio

class EmbedCreator:
    def __init__(self,title,description,url,thumbnail,color) -> None:
        self.title = title
        self.description = description
        self.url = url
        self.thumbnail = thumbnail
        self.color = color

    async def getEmbed(self):
        twitImg = await asyncio.get_running_loop().run_in_executor(None,TwitterImageGrabber.getImage)
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