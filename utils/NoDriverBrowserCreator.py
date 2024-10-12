import requests
import random
import nodriver as uc
import globals
import asyncio
import ctypes, os
import platform
import psutil
import logging
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
from nodriver import *

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

def KillUnconncetedBrowsers():
    PROCNAMES = ["google-chrome",
                "chromium",
                "chromium-browser",
                "chrome",
                "google-chrome-stable"]
    numBrowserProcesses = 0
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() in PROCNAMES:
            numBrowserProcesses = numBrowserProcesses + 1
            try:
                proc.terminate()
            except Exception as e:
                proc.kill()
                logger.warning(e)
    if numBrowserProcesses > 0:
        logger.info(f"Tried to kill {numBrowserProcesses} browser processes.")

def getUserAgent():
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/127.0.2651.105"
        try:
            page = requests.get('https://jnrbsn.github.io/user-agents/user-agents.json')
            userAgentsJson = page.json()
            userAgent = random.choice(userAgentsJson)
            page.close()
        except:
            logger.warning("Trouble getting user agent from jnrbsn's github. Using default")
        return userAgent

async def GetBrowser(proxy=""):
    while globals.browserOpen:
        await asyncio.sleep(2 * Constants.NODRIVER_WAIT_MULTIPLIER)
    try:
        globals.browserOpen = True
        await asyncio.sleep(1 * Constants.NODRIVER_WAIT_MULTIPLIER)
        toSandbox = not IsRoot()
        toHeadless = False if platform.system() == "Linux" else True
        if proxy:
            browser = await uc.start(sandbox=toSandbox,
                                headless=toHeadless,
                                browser_args=[f'--proxy-server={proxy}','--mute-audio','--disable-3d-apis','--disable-dev-shm-usage','--disable-gpu','--disable-blink-features=AutomationControlled'],
                                retries = Constants.NODRIVER_BROWSER_CONNECT_RETRIES)
        else:
            browser = await uc.start(sandbox=toSandbox,
                                headless=toHeadless,
                                retries = Constants.NODRIVER_BROWSER_CONNECT_RETRIES)
    except Exception as e:
        logger.warning(f"error creating browser in GetBrowser: {e}")
        await asyncio.sleep(1 *  Constants.NODRIVER_WAIT_MULTIPLIER)
        KillUnconncetedBrowsers()
        await asyncio.sleep(1 *  Constants.NODRIVER_WAIT_MULTIPLIER)
        globals.browserOpen = False
    return browser

# Taken from https://github.com/ultrafunkamsterdam/nodriver/blob/1bb6003c7f0db4d3ec05fdf3fc8c8e0804260103/nodriver/core/config.py#L240
def IsRoot():
    """
    helper function to determine if user trying to launch chrome
    under linux as root, which needs some alternative handling
    :return:
    :rtype:
    """

    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0