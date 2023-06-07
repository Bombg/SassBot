from typing import Any
import tanjun
from datetime import datetime
import time

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
            print("didn't get right ctx for logger")
        self.file.close()
        return self.func(*args,**kwds)