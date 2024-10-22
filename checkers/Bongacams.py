import requests
import time
from bs4 import BeautifulSoup
import json
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
from utils.NoDriverBrowserCreator import getUserAgent
import logging
from utils.StaticMethods import GetThumbnail
from utils.StaticMethods import GetProxies

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

def isModelOnline(bcUserName):
    title = Constants.bcDefaultTitle
    tempThumbUrl = ""
    isOnline = False
    icon = Constants.defaultIcon
    agent = getUserAgent()
    headers = {"User-Agent": agent}
    try:
        if Constants.BC_PROXY:
            page = requests.get(f'https://bongacams.com/{bcUserName}',headers=headers, proxies=GetProxies(Constants.BC_PROXY))
        else:
            page = requests.get(f'https://bongacams.com/{bcUserName}',headers=headers)
        time.sleep(1)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            bcJson = []
            roomJsons = soup.find_all("script", type="application/json")
            for roomJson in roomJsons:
                if 'chatTopicOptions' in roomJson.text:
                    bcJson = json.loads(roomJson.text)
                    break
            if bcJson: 
                if bcJson["chatTopicOptions"]["currentTopic"]:
                    title = bcJson["chatTopicOptions"]["currentTopic"]
                    title = title.replace('\u200b', '')
                    title = title.replace('\r', '')
                    title = title.replace('\n', '')
                icon = bcJson['chatHeaderOptions']['profileImage']
                icon = "https:" + icon
                isOnline = not bcJson['chatShowStatusOptions']['isOffline']
    except requests.exceptions.ConnectTimeout:
        logger.warning("connection timed out to Bongacams. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to Bomgacams")
    thumbUrl = GetThumbnail(tempThumbUrl, Constants.bcThumbnail)
    return isOnline, title, thumbUrl, icon
