import miru
import hikari
from utils.Database import Database
from datetime import timedelta
import plugins.commands as commands
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
import tanjun
import random

class ConfessionReView(miru.View):
    def __init__(self, *, timeout: float | int | timedelta | None = 120, autodefer: bool = True, confessionId, tanCtx: tanjun.abc.SlashContext, confession:str,rest: hikari.impl.RESTClientImpl,title) -> None:
        self.db = Database()
        self.confessionId = confessionId
        self.tanCtx = tanCtx
        self.confession = confession
        self.rest = rest
        self.title = title
        super().__init__(timeout=timeout, autodefer=autodefer)
    @miru.button(label="Approve&Finish", style=hikari.ButtonStyle.SUCCESS)
    async def approveButton(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        self.db.reviewConfession(self.confessionId,1,ctx.member.id,ctx.member.display_name)
        content = f"## {self.confessionId}:{self.title}\n``` {self.confession} ```"
        await self.rest.create_message(channel=Constants.CONFESSTION_CHANNEL_ID, content=content)
        self.stop()
    @miru.button(label="Approve&Next", style=hikari.ButtonStyle.SUCCESS)
    async def approveAndReview(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        self.db.reviewConfession(self.confessionId,1,ctx.member.id,ctx.member.display_name)
        content = f"## {self.confessionId}:{self.title}\n``` {self.confession} ```"
        await self.rest.create_message(channel=Constants.CONFESSTION_CHANNEL_ID, content=content)
        self.stop()
        await commands.confessReview(self.tanCtx, self.rest)
    @miru.button(label="Pass&Next", style=hikari.ButtonStyle.SECONDARY)
    async def passAndReview(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        self.stop()
        await commands.confessReview(self.tanCtx, self.rest)
    @miru.button(label="Deny&Finish", style=hikari.ButtonStyle.DANGER)
    async def denyButton(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        self.db.reviewConfession(self.confessionId,0,ctx.member.id,ctx.member.display_name)
        self.stop()
    @miru.button(label="Deny&Next", style=hikari.ButtonStyle.DANGER)
    async def denyAndReview(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        self.db.reviewConfession(self.confessionId,0,ctx.member.id,ctx.member.display_name)
        self.stop()
        await commands.confessReview(self.tanCtx, self.rest)

class ConfessionModal(miru.Modal):
    confTitle = miru.TextInput(label="Title", placeholder="Enter your title!", required=True,max_length=75)
    confess = miru.TextInput(label="Confession/Question",placeholder="Enter your Confession/Question here", style=hikari.TextInputStyle.PARAGRAPH, required=True, max_length=1900)
    async def callback(self, ctx: miru.ModalContext) -> None:
        db = Database()
        db.addConfession(self.confess.value, self.confTitle.value)
        await ctx.respond(f"Submitted Confession: \n```{self.confess.value}```\n This will be posted once it's reveiwed by a mod", flags=hikari.MessageFlag.EPHEMERAL)

class ConfessionModalView(miru.View):
    @miru.button(label="Click to Submit", style=hikari.ButtonStyle.PRIMARY)
    async def modal_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        modal = ConfessionModal(title="Submit Confession/Question")
        # await ctx.respond_with_modal(modal)
        await modal.send(ctx.interaction)

def createConfessionEmbed(confessionId, confession, title):
    color = random.randrange(0, 2**24)
    color = hex(color)
    embed = (
            hikari.Embed(
            title = str(confessionId) + ": " + title ,
            color = color
            )
        ).add_field(name="Confession/Question", value=confession)
    return embed