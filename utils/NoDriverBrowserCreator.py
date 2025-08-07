import requests
import random
import nodriver as uc
import globals
import asyncio
import ctypes, os
import platform
import psutil
import logging
from DefaultConstants import Settings as Settings
from nodriver import *

baseSettings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

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
        logger.debug(f"Tried to kill {numBrowserProcesses} browser processes.")

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
        await asyncio.sleep(2 * baseSettings.NODRIVER_WAIT_MULTIPLIER)
    try:
        globals.browserOpen = True
        await asyncio.sleep(1 * baseSettings.NODRIVER_WAIT_MULTIPLIER)
        toSandbox = not IsRoot()
        toHeadless = False if platform.system() == "Linux" else True
        dataDir = "/ndTemp" if platform.system() == "Linux" else None
        if proxy:
            browser = await uc.start(sandbox=toSandbox,
                                headless=toHeadless,
                                browser_args=[f'--proxy-server={proxy}','--mute-audio','--disable-3d-apis','--disable-dev-shm-usage','--disable-gpu'],
                                retries = baseSettings.NODRIVER_BROWSER_CONNECT_RETRIES,
                                user_data_dir=dataDir
                                )
        else:
            browser = await uc.start(sandbox=toSandbox,
                                headless=toHeadless,
                                browser_args=['--mute-audio','--disable-3d-apis','--disable-dev-shm-usage','--disable-gpu'],
                                retries = baseSettings.NODRIVER_BROWSER_CONNECT_RETRIES,
                                user_data_dir=dataDir
                                )
        return browser
    except Exception as e:
        logger.warning(f"error creating browser in GetBrowser: {e}")
        await asyncio.sleep(1 *  baseSettings.NODRIVER_WAIT_MULTIPLIER)
        KillUnconncetedBrowsers()
        await asyncio.sleep(1 *  baseSettings.NODRIVER_WAIT_MULTIPLIER)
        globals.browserOpen = False

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

async def CloseNDBrowser(browser, page):
    await page.close()
    await asyncio.sleep(1*baseSettings.NODRIVER_WAIT_MULTIPLIER)
    browser.stop()
    await asyncio.sleep(1*baseSettings.NODRIVER_WAIT_MULTIPLIER)
    if platform.system() == "Linux":
        KillUnconncetedBrowsers()
    globals.browserOpen = False