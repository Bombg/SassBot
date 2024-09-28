import os
import platform

from bot import build_bot

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    if platform.system() == "Linux":
        os.system('Xvfb $DISPLAY -screen $DISPLAY 1280x1024x16 & export DISPLAY=:99')
    build_bot().run()
