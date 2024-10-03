import requests
import time
from bs4 import BeautifulSoup
import json
from Constants import Constants
from NoDriverBrowserCreator import getUserAgent

def isModelOnline(bcUserName):
    title = Constants.bcDefaultTitle
    thumbUrl = ''
    isOnline = False
    icon = 'images/errIcon.png'
    agent = getUserAgent()
    headers = {"User-Agent": agent}
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
    page.close()
    return isOnline, title, thumbUrl, icon


    