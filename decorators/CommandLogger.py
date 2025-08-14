import tanjun
from datetime import datetime
import time
import logging
from DefaultConstants import Settings as Settings
import miru
import functools

baseSettings = Settings()
logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

def CommandLogger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        file = open("commandLogs.txt", 'a')
        date = datetime.fromtimestamp(time.time())
        ctx = args[0]
        if isinstance(ctx, tanjun.abc.SlashContext) or isinstance(ctx, miru.ViewContext):
            info = f"{date}:{ctx.member.display_name}:{ctx.member.id}:{func.__name__}\n"
            file.write(info)
            logger.info(f"COMMAND: {info}")
        else:
            logger.error("didn't get right ctx for command logger")
        file.close()
        return func(*args, **kwds)
    return wrapper