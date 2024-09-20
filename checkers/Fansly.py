import time
from Constants import Constants
import StaticMethods
import asyncio
import nodriver as uc

def isModelOnline(fansUserName):
    isOnline, title, thumbUrl, icon = uc.loop().run_until_complete(GetOnlineStatus(fansUserName))
    return isOnline, title, thumbUrl, icon

async def GetOnlineStatus(fansUserName):
    fansUrl = f"https://fansly.com/{fansUserName}"
    thumbUrl = ""
    title = Constants.fansDefaultTitle
    browser = await uc.start(
        headless=True,
        sandbox=False,
    )
    page = await browser.get(fansUrl)
    await asyncio.sleep(5)
    await ClickEnterButton(page)
    isOnline = await IsLiveBadge(page)
    await asyncio.sleep(2)
    icon = await GetIcon(page)
    await page.save_screenshot("Fansscreenshot.png")
    return isOnline, title, thumbUrl, icon

async def ClickEnterButton(page:uc.Tab):
    try:
        enterBtn = await page.find("Enter",best_match=True)
        if enterBtn:
            await enterBtn.click()
            await asyncio.sleep(5)
    except TimeoutError:
        pass

async def IsLiveBadge(page:uc.Tab):
    live = False
    try:
        liveBadge = await page.find("live-badge bold font-size-sm", best_match=True)
        if liveBadge:
            live = True
    except TimeoutError:
        pass
    return live

async def GetIcon(page:uc.Tab):
    icon = 'images/errIcon.png'
    try:
        iconElements = await page.find_all("image cover")
        await iconElements[1].click()
        await asyncio.sleep(2)
        iconElement = await page.find("image-overlay-flex", best_match=True)
        await iconElement.save_screenshot( "images/fansIcon.jpg")
        icon = "images/fansIcon.jpg"
    except:
        pass
    return icon
