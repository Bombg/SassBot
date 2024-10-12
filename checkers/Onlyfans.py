try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
import re
import asyncio
import nodriver as uc
import utils.NoDriverBrowserCreator as ndb
import globals
import logging
from utils.StaticMethods import GetThumbnail

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

async def isModelOnline(ofUserName):
    isOnline = False
    ofUrl = f"https://onlyfans.com/{ofUserName}"
    title = Constants.ofDefaultTitle
    tempThumbUrl = ""
    icon = Constants.defaultIcon
    try:
        browser = await ndb.GetBrowser(proxy=Constants.OF_PROXY)
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        page = await browser.get(ofUrl, new_window=True)
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        await page.save_screenshot("Ofscreenshot.jpg")
        isOnline = await IsLiveBadge(page)
        icon  = await GetIcon(page)
        await page.close()
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        browser.stop()
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        globals.browserOpen = False
    except Exception as e:
        logger.warning(f"Error getting browser for Onylyfans: {e}")
        globals.browserOpen = False
    thumbUrl = GetThumbnail(tempThumbUrl, Constants.ofThumbnail)
    return isOnline, title, thumbUrl, icon

async def GetIcon(page:uc.Tab):
    icon = Constants.defaultIcon
    reString = r'^https:\/\/.+avatar.jpg$'
    try:
        imageElements = await page.find_all("data-v-325c6981")
        for element in imageElements:
            if element.attrs.get("src") and re.search(reString, element.attrs.get("src")):
                icon = element.attrs.get("src")
    except asyncio.exceptions.TimeoutError:
        pass
    return icon

async def IsLiveBadge(page:uc.Tab):
    live = False
    try:
        liveBadge = await page.find("g-avatar__icon m-live", best_match=True)
        if liveBadge:
            live = True
    except asyncio.exceptions.TimeoutError:
        pass
    return live