import requests
import json
import time
from DefaultConstants import Settings as Settings
from utils.NoDriverBrowserCreator import getUserAgent
import logging
from utils.StaticMethods import GetThumbnail
from utils.StaticMethods import GetProxies

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
            page = requests.get(f'https://stripchat.com/api/vr/v2/models/username/{scUserName}', headers=headers, proxies=GetProxies(baseSettings.SC_PROXY))
        else:
            page = requests.get(f'https://stripchat.com/api/vr/v2/models/username/{scUserName}', headers=headers)
        time.sleep(1)
        if page.status_code == 200:
            try:
                scJson = page.json()
                isOnline = True if scJson['model']['status']  != 'off' else False
                icon = scJson['model']['avatarUrl']
                title = scJson['goal']['description'] if scJson['goal']['description'] else baseSettings.scDefaultTitle
                tempThumbUrl = scJson['model']['previewUrl'] + "?" + str(int(time.time()))
            except json.decoder.JSONDecodeError:
                pass
    except requests.exceptions.ConnectTimeout:
        logger.warning("connection timed out to Stripchat. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to Stripchat")
    thumbUrl = GetThumbnail(tempThumbUrl, baseSettings.scThumbnail)
    return isOnline, title, thumbUrl, icon