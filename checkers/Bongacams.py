import requests
import time
from bs4 import BeautifulSoup
import json
from Constants import Constants
from NoDriverBrowserCreator import getUserAgent
import logging

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

def isModelOnline(bcUserName):
    title = Constants.bcDefaultTitle
    thumbUrl = ''
    isOnline = False
    icon = 'images/errIcon.png'
    agent = getUserAgent()
    headers = {"User-Agent": agent}
    try:
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
    return isOnline, title, thumbUrl, icon


    