import os
import platform
import logging
from pyvirtualdisplay import Display
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
from utils.bot import build_bot
import colorlog

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
	'%(log_color)s%(bold)s%(levelname)s:%(name)s:%(message)s'))
handlers = [handler]
logging.basicConfig(level=Constants.OTHER_LIBRARIES_LOG_LEVEL, handlers=handlers)

if os.name != "nt":
    import uvloop
    uvloop.install()

if __name__ == "__main__":
    if platform.system() == "Linux":
        logger.info("Opening Display")
        display = Display(visible=0, size=(1080,720))
        display.start()

    build_bot().run()

    if platform.system() == "Linux":
        logger.info("Closing Display")
        display.stop()
    
