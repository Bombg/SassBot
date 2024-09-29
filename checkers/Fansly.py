from Constants import Constants
import asyncio
import nodriver as uc
import NoDriverBrowserCreator as ndb
import globals
import multiprocessing

def isModelOnline(fansUserName):
    # queue = multiprocessing.Manager()
    # returnDict = queue.dict()
    # p = multiprocessing.Process(target=process, args=(fansUserName, returnDict))
    # p.start()
    # p.join()
    # isOnline = returnDict.get("isOnline")
    # title = returnDict.get("title")
    # thumbUrl = returnDict.get("thumbUrl")
    # icon = returnDict.get("icon")
    # p.terminate()
    isOnline, title, thumbUrl, icon = uc.loop().run_until_complete(GetOnlineStatus(fansUserName))
    return isOnline, title, thumbUrl, icon

def process(fansUserName, returnDict):
    isOnline, title, thumbUrl, icon = uc.loop().run_until_complete(GetOnlineStatus(fansUserName))
    returnDict["isOnline"] = isOnline
    returnDict["title"] = title
    returnDict['thumbUrl'] = thumbUrl
    returnDict['icon'] = icon

async def GetOnlineStatus(fansUserName):
    fansUrl = f"https://fansly.com/{fansUserName}"
    thumbUrl = ""
    title = Constants.fansDefaultTitle
    isOnline = False
    icon = 'images/errIcon.png'
    try:
        browser = await ndb.GetBrowser(proxy=Constants.FANS_PROXY)
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        page = await browser.get(fansUrl)
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        await ClickEnterButton(page)
        isOnline = await IsLiveBadge(page)
        icon = await GetIcon(page)
        await page.save_screenshot("Fansscreenshot.jpg")
        await page.close()
        await asyncio.sleep(.5*Constants.NODRIVER_WAIT_MULTIPLIER)
        browser.stop()
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        globals.browserOpen = False
    except Exception as e:
        print(f"Error when getting browser for Fansly: {e}")
        globals.browserOpen = False
    return isOnline, title, thumbUrl, icon

async def ClickEnterButton(page:uc.Tab):
    try:
        enterBtn = await page.find("Enter",best_match=True)
        if enterBtn:
            await enterBtn.click()
            await asyncio.sleep(.5 * Constants.NODRIVER_WAIT_MULTIPLIER)
    except :
        pass

async def IsLiveBadge(page:uc.Tab):
    live = False
    try:
        liveBadge = await page.find("live-badge bold font-size-sm", best_match=True)
        if liveBadge:
            live = True
    except :
        pass
    return live

async def GetIcon(page:uc.Tab):
    icon = 'images/errIcon.png'
    try:
        iconElements = await page.find_all("image cover")
        await iconElements[1].click()
        await asyncio.sleep(.5 * Constants.NODRIVER_WAIT_MULTIPLIER)
        iconElement = await page.find("image-overlay-flex", best_match=True)
        await iconElement.save_screenshot( "images/fansIcon.jpg")
        icon = "images/fansIcon.jpg"
    except:
        pass
    return icon
