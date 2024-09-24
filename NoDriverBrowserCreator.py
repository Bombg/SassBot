import requests
import random
import nodriver as uc
import globals
import asyncio
import ctypes, os
import platform
import psutil
import StaticMethods

def killPotentialZombies():
    PROCNAMES = ["google-chrome",
                "chromium",
                "chromium-browser",
                "chrome",
                "google-chrome-stable"]
    numZombies = 0
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() in PROCNAMES:
            numZombies = numZombies + 1
            proc.kill()
    if numZombies > 0:
        print(f"Killed {numZombies} zombies.")
    if numZombies > 15:
            StaticMethods.rebootServer()

def getUserAgent():
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/127.0.2651.105"
        try:
            page = requests.get('https://jnrbsn.github.io/user-agents/user-agents.json')
            userAgentsJson = page.json()
            userAgent = random.choice(userAgentsJson)
        except:
            print("Trouble getting user agent from jnrbsn's github. Using default")
        return userAgent

async def GetBrowser():
    while globals.browserOpen:
        await asyncio.sleep(20)
    # userAgent = getUserAgent()
    # browser_args=[f'user-agent={userAgent}']
    toSandbox = not IsRoot()
    toHeadless = False if platform.system() == "Linux" else True
    try:
        globals.browserOpen = True
        if platform.system() == "Linux":killPotentialZombies()
        browser = await uc.start(
        headless=toHeadless,
        sandbox= toSandbox
    )
    except Exception as e:
        print(f"error creating browser in GetBrowser: {e}")
        if platform.system() == "Linux":killPotentialZombies()
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