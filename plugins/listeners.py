import hikari
import alluka
import tanjun
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants 
from datetime import datetime
import time
from utils.MiruViews import ConnectKick
from utils.MiruViews import BanAppealButton

component = tanjun.Component()

@component.with_listener(hikari.StartedEvent)
async def startup_views(event: hikari.StartedEvent) -> None:
    view = ConnectKick()
    await view.start()
    banView = BanAppealButton()
    await banView.start()

@component.with_listener(hikari.MessageDeleteEvent)
async def printDelete(event: hikari.MessageDeleteEvent, rest: alluka.Injected[hikari.impl.RESTClientImpl]):
    try:
        if event.old_message.author.is_bot: return
        file = open("deletedMessageLogs.txt", 'a')
        date = datetime.fromtimestamp(time.time())
        file.write(f"{date} Author: {event.old_message.author.id}-{event.old_message.author.username} - deleted: {event.old_message.content} or {event.old_message.embeds} in {event.channel_id} \n")
        file.close()
    except(AttributeError):
        pass

@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())