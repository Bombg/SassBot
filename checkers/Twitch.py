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

def isModelOnline(twitchChannelName: str):
    twitchChannelName = twitchChannelName.lower()
    title = "placeholder twitch title"
    tempThumbUrl = ''
    isOnline = False
    icon = Constants.defaultIcon
    try:
        tempThumbUrl = f'https://static-cdn.jtvnw.net/previews-ttv/live_user_{twitchChannelName}-640x360.jpg'
        thumbUrlReq = requests.get(tempThumbUrl,allow_redirects=True)
        time.sleep(1)
        if tempThumbUrl == thumbUrlReq.url:
            isOnline = True
            page = requests.get(f'https://www.twitch.tv/{twitchChannelName}')
            time.sleep(1)
            soup = BeautifulSoup(page.content, "html.parser")
            title = getTitle(soup)
            reticon = getIcon(soup)
            if reticon:
                icon = reticon
            tempThumbUrl = tempThumbUrl + "?" + str(int(time.time()))
    except requests.exceptions.ConnectTimeout:
        logger.warning("connection timed out to Twitch. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to Twitch")
    thumbUrl = GetThumbnail(tempThumbUrl, Constants.twitchThumbnail)
    return isOnline, title, thumbUrl, icon

def getIcon(soup):
    icon = 0
    try:
        icon = soup.find("meta", property="og:image")['content']
    except IndexError:
        pass
    return icon

def getTitle(soup):
    title = "placeholder twitch title"
    try:
        title = soup.find("meta", property="og:description")['content']
    except IndexError:
        pass
    return title
