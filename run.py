import os
import platform
import subprocess

from bot import build_bot

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    if platform.system() == "Linux":
        subprocess.run('Xvfb $DISPLAY -screen $DISPLAY 1280x1024x16 & export DISPLAY=:99')
    build_bot().run()
