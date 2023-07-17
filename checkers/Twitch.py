import requests
import json
from bs4 import BeautifulSoup
import time
import StaticMethods

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
        title = twitchJson['description']
        thumbUrl = twitchJson['thumbnailUrl'][2]
        reticon = getIcon(soup)
        if reticon:
            icon = reticon
        rerun = StaticMethods.isRerun(title)
        if not rerun:
            isOnline = twitchJson['publication']['isLiveBroadcast']
    return isOnline, title, thumbUrl, icon

def getTwitchJson(soup):
    twitchJson = 0
    try:
        firstSplit = soup.prettify().split('<script type=\"application/ld+json\">\n    [')
        jsonSplit = firstSplit[1].split(']\n   </script>')
        twitchJson = json.loads(jsonSplit[0])
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
