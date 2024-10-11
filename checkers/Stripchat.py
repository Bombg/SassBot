import requests
import json
import time
from Constants import Constants
from NoDriverBrowserCreator import getUserAgent
import logging

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

def isModelOnline(scUserName):
    title = Constants.scDefaultTitle
    thumbUrl = ''
    isOnline = False
    icon = 'images/errIcon.png'
    agent = getUserAgent()
    headers = {"User-Agent": agent}
    try:
        page = requests.get(f'https://stripchat.com/api/vr/v2/models/username/{scUserName}', headers=headers)
        time.sleep(1)
        if page.status_code == 200:
            try:
                scJson = page.json()
                isOnline = True if scJson['model']['status']  != 'off' else False
                icon = scJson['model']['avatarUrl']
                title = scJson['goal']['description'] if scJson['goal']['description'] else Constants.scDefaultTitle
                thumbUrl = scJson['model']['previewUrl'] + "?" + str(int(time.time()))
            except json.decoder.JSONDecodeError:
                pass
    except requests.exceptions.ConnectTimeout:
        logger.warning("connection timed out to Stripchat. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to Stripchat")
    return isOnline, title, thumbUrl, icon