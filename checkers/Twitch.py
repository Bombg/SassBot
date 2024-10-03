import requests
import json
from bs4 import BeautifulSoup
import time

def isModelOnline(twitchChannelName):
    title = "placeholder twitch title"
    thumbUrl = ''
    isOnline = False
    icon = 'images/errIcon.png'
    page = requests.get(f'https://www.twitch.tv/{twitchChannelName}')
    time.sleep(1)
    soup = BeautifulSoup(page.content, "html.parser")
    twitchJson = getTwitchJson(soup)
    if twitchJson:
        title = twitchJson['@graph'][0]['description']
        thumbUrl = twitchJson['@graph'][0]['thumbnailUrl'][2]
        reticon = getIcon(soup)
        if reticon:
            icon = reticon
        thumbUrlReq = requests.get(thumbUrl,allow_redirects=True)
        time.sleep(1)
        isOnlineJson = twitchJson['@graph'][0]['publication']['isLiveBroadcast']
        if isOnlineJson and thumbUrl == thumbUrlReq.url:
            isOnline = True
    page.close()
    return isOnline, title, thumbUrl, icon

def getTwitchJson(soup):
    twitchJson = 0
    try:
        twitchJson = soup.find_all("script", type="application/ld+json")
        twitchJson = json.loads(twitchJson[0].text)
    except IndexError:
        pass
    return twitchJson

def getIcon(soup):
    icon = 0
    try:
        icon = soup.find("meta", property="og:image")['content']
    except IndexError:
        pass
    return icon
