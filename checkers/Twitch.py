import requests
import json
from bs4 import BeautifulSoup
import time
import logging
from DefaultConstants import Settings as Settings
from utils.StaticMethods import GetThumbnail

baseSettings = Settings()
logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

def isModelOnline(twitchChannelName: str):
    twitchChannelName = twitchChannelName.lower()
    title = "placeholder twitch title"
    tempThumbUrl = ''
    isOnline = False
    icon = baseSettings.defaultIcon
    try:
        isOnline = IsOnline(twitchChannelName)
        time.sleep(1)
        if isOnline:
            isOnline = True
            page = requests.get(f'https://www.twitch.tv/{twitchChannelName}')
            tempThumbUrl = f'https://static-cdn.jtvnw.net/previews-ttv/live_user_{twitchChannelName}-640x360.jpg'
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
    except TypeError:
        logger.warning("twitch user banned or doesn't exist")
    thumbUrl = GetThumbnail(tempThumbUrl, baseSettings.twitchThumbnail)
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

def IsOnline(channelName):
    url = "https://gql.twitch.tv/gql"
    query = "query {\n  user(login: \""+ channelName +"\") {\n    stream {\n      id\n    }\n  }\n}"
    return True if requests.request("POST", url, json={"query": query, "variables": {}}, headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"}).json()["data"]["user"]["stream"] else False
