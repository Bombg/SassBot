import os
import hikari
import time

from bot import build_bot

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    try:
        build_bot().run()
    except hikari.errors.GatewayConnectionError:
        time.sleep(30)
        build_bot().run()
