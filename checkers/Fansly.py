from DefaultConstants import Settings as Settings
import asyncio
import nodriver as uc
import utils.NoDriverBrowserCreator as ndb
import globals
import logging
from utils.StaticMethods import GetThumbnail

baseSettings = Settings()
logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

async def isModelOnline(fansUserName):
    fansUrl = f"https://fansly.com/{fansUserName}"
    tempThumbUrl = ""
    title = baseSettings.fansDefaultTitle
    isOnline = False
    icon = baseSettings.defaultIcon
    try:
        browser = await ndb.GetBrowser(proxy=baseSettings.FANS_PROXY)
        await asyncio.sleep(1*baseSettings.NODRIVER_WAIT_MULTIPLIER)
        page = await browser.get(fansUrl)
        await asyncio.sleep(1*baseSettings.NODRIVER_WAIT_MULTIPLIER)
        await ClickEnterButton(page)
        isOnline = await IsLiveBadge(page)
        icon = await GetIcon(page)
        await page.save_screenshot("Fansscreenshot.jpg")
        await ndb.CloseNDBrowser(browser,page)
    except Exception as e:
        logger.warning(f"Error when getting browser for Fansly: {e}")
        globals.browserOpen = False
    thumbUrl = GetThumbnail(tempThumbUrl, baseSettings.fansThumbnail)
    return isOnline, title, thumbUrl, icon

async def ClickEnterButton(page:uc.Tab):
    try:
        enterBtn = await page.find("Enter",best_match=True)
        if enterBtn:
            await enterBtn.click()
            await asyncio.sleep(.5 * baseSettings.NODRIVER_WAIT_MULTIPLIER)
    except asyncio.exceptions.TimeoutError:
        pass

async def IsLiveBadge(page:uc.Tab):
    live = False
    try:
        liveBadge = await page.find("live-badge bold font-size-sm", best_match=True)
        if liveBadge:
            live = True
    except asyncio.exceptions.TimeoutError:
        pass
    return live

async def GetIcon(page:uc.Tab):
    icon = baseSettings.defaultIcon
    try:
        iconElements = await page.find_all("image cover")
        await iconElements[1].click()
        await asyncio.sleep(.5 * baseSettings.NODRIVER_WAIT_MULTIPLIER)
        iconElement = await page.find("image-overlay-flex", best_match=True)
        await iconElement.save_screenshot( "images/fansIcon.jpg")
        icon = "images/fansIcon.jpg"
    except asyncio.exceptions.TimeoutError:
        pass
    return icon
