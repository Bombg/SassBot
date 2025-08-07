import hikari
import tanjun
from DefaultConstants import Settings as Settings
import miru

baseSettings = Settings()

def getToken():
    token = baseSettings.SECRET
    return str(token)

def build_bot() -> hikari.GatewayBot:
    TOKEN = getToken()
    bot = hikari.GatewayBot(TOKEN,
                            intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT | hikari.Intents.GUILD_MEMBERS | hikari.Intents.GUILD_PRESENCES
                            )
    make_client(bot)
    miru.install(bot)
    return bot

def make_client(bot: hikari.GatewayBot) -> tanjun.Client:
    client = (
        tanjun.Client.from_gateway_bot(
            bot,
            mention_prefix=True,
            declare_global_commands=baseSettings.GUILD_ID
        )
    ).add_prefix("!")
    client.load_modules("plugins.checks")
    client.load_modules("plugins.commands")
    client.load_modules("plugins.listeners")
    return client