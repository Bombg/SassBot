import os

from bot import build_bot

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    build_bot().run()
