import os
import platform
import subprocess
from pyvirtualdisplay import Display

from bot import build_bot

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    if platform.system() == "Linux":
        display = Display(visible=0, size=(1080,720))
        display.start()

    build_bot().run()

    if platform.system() == "Linux":
        display.stop()
    
