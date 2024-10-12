from typing import Any
import tanjun
from datetime import datetime
import time
import logging
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

class CommandLogger:
    def __init__(self, func) -> None:
        self.func = func
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.file = open("commandLogs.txt", 'a')
        self.date = datetime.fromtimestamp(time.time())
        ctx = args[0]
        if isinstance(ctx, tanjun.abc.SlashContext):
            self.file.write(f"{self.date} - {self.func.__name__} - used by {ctx.member.id} aka {ctx.member.display_name}\n")
        else:
            logger.error("didn't get right ctx for command logger")
        self.file.close()
        return self.func(*args,**kwds)