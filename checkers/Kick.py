import asyncio
import nodriver as uc
import json
import time
import NoDriverBrowserCreator as ndb

def isModelOnline(kickUserName):
    isOnline, title, thumbUrl, icon = uc.loop().run_until_complete(GetOnlineStatus(kickUserName))
    return isOnline, title, thumbUrl, icon

async def GetOnlineStatus(kickUserName):
    isOnline, title, thumbUrl, icon = setDefaultStreamValues()
    apiUrl = f"https://kick.com/api/v1/channels/{kickUserName}"
    try:
        browser = await ndb.GetBrowser()
        await asyncio.sleep(10)
        page = await browser.get(apiUrl)
        await asyncio.sleep(30)
        await page.save_screenshot("KickScreenshot.png")
        content = await page.get_content()
        content = content.split('<body>')
        if len(content) < 2:
            print("error with kick checker. user is banned,wrong username supplied, or cloudflare bot detection")
        else:
            jsonText = content[1].split('</body></html>')
            isOnline, title, thumbUrl, icon = getStreamInfo(jsonText)
        await page.close()
        ndb.killBrowser(browser)
    except Exception as e:
        print(f"error getting browser for Kick: {e}")
    return isOnline, title, thumbUrl, icon

def setDefaultStreamValues():
    isOnline = False
    title = "place holder kick title, this should never show up unless coder fucked up"
    thumbUrl = ""
    icon = 'images/errIcon.png'
    return isOnline, title, thumbUrl, icon

def getStreamInfo(jsonText):
    isOnline, title, thumbUrl, icon = setDefaultStreamValues()
    try:
        results = json.loads(jsonText[0])
        if results['livestream']:
            title = results['livestream']['session_title']
            title = title.replace("&amp;","&")
            thumbUrl = results['livestream']['thumbnail']['url']+ "?" + str(int(time.time()))
            icon = results['user']['profile_pic']
            isOnline = True
    except json.decoder.JSONDecodeError:
        print("no json at kick api, bot detection or site down?")
    return isOnline,title,thumbUrl,icon
