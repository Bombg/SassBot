import os
import hikari
import time

from bot import build_bot

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    while True:
        try:
            build_bot().run()
        except hikari.errors.GatewayConnectionError:
            print("no internet, sleeping for 30s and then restarting bot")
            time.sleep(30)
