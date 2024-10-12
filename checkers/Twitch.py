import requests
import json
from bs4 import BeautifulSoup
import time
import logging
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
from utils.StaticMethods import GetThumbnail

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

def isModelOnline(twitchChannelName):
    title = "placeholder twitch title"
    tempThumbUrl = ''
    isOnline = False
    icon = Constants.defaultIcon
    try:
        page = requests.get(f'https://www.twitch.tv/{twitchChannelName}')
        time.sleep(1)
        soup = BeautifulSoup(page.content, "html.parser")
        twitchJson = getTwitchJson(soup)
        if twitchJson:
            title = twitchJson['@graph'][0]['description']
            tempThumbUrl = twitchJson['@graph'][0]['thumbnailUrl'][2]
            reticon = getIcon(soup)
            if reticon:
                icon = reticon
            thumbUrlReq = requests.get(tempThumbUrl,allow_redirects=True)
            time.sleep(1)
            isOnlineJson = twitchJson['@graph'][0]['publication']['isLiveBroadcast']
            if isOnlineJson and tempThumbUrl == thumbUrlReq.url:
                tempThumbUrl = tempThumbUrl + "?" + str(int(time.time()))
                isOnline = True
    except requests.exceptions.ConnectTimeout:
        logger.warning("connection timed out to Twitch. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to Twitch")
    thumbUrl = GetThumbnail(tempThumbUrl, Constants.twitchThumbnail)
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
