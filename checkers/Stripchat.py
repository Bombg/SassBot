import requests
import json
import time
from DefaultConstants import Settings as Settings
import logging
from utils.StaticMethods import GetThumbnail
import tls_client
from utils.StaticMethods import GetProxies
from utils.NoDriverBrowserCreator import getUserAgent

baseSettings = Settings()
logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

def isModelOnline(scUserName):
    title = baseSettings.scDefaultTitle
    tempThumbUrl = ''
    isOnline = False
    icon = baseSettings.defaultIcon
    agent = getUserAgent()
    headers = {"User-Agent": agent}
    try:
        if baseSettings.SC_PROXY:
            page = requests.get(f"https://stripchat.com/api/front/v2/models/username/{scUserName}/cam", headers=headers, proxies=GetProxies(baseSettings.SC_PROXY))
        else:
            page = requests.get(f"https://stripchat.com/api/front/v2/models/username/{scUserName}/cam",headers=headers)
        time.sleep(1)
        if page.status_code == 200:
            try:
                scJson = page.json()
                isOnline = True if scJson["user"]["user"]["status"] != "off" else False
                icon = scJson["user"]["user"]["avatarUrl"]
                title = scJson['cam']["goal"]["description"] if scJson['cam']["goal"]["description"] else baseSettings.scDefaultTitle
                tempThumbUrl = scJson['user']['user']['previewUrl'] + "?" + str(int(time.time()))
                thumbUrl = GetThumbnail(tempThumbUrl, baseSettings.scThumbnail)
            except json.decoder.JSONDecodeError:
                pass
    except requests.exceptions.ConnectTimeout:
        logger.warning("connection timed out to Stripchat. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to Stripchat")
    thumbUrl = GetThumbnail(tempThumbUrl, baseSettings.scThumbnail)
    return isOnline, title, thumbUrl, icon