import time
import requests
from Constants import Constants
from bs4 import BeautifulSoup
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

def isModelOnline(epUserName):
    isOnline = False
    title = Constants.epDefaultTitle
    thumbUrl = ""
    icon = 'images/errIcon.png'
    try:
        request = requests.get(f"https://eplay.com/{epUserName}")
        time.sleep(1)
        soup = BeautifulSoup(request.content, "html.parser")
        profileJson = soup.find_all("script", type="application/json")
        profileJson = json.loads(profileJson[0].text)
        isOnline = profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["live"]
        title =  profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["title"]
        thumbUrl = profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["ss"] + "?" + str(int(time.time()))
        icon =  profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["avatar"]
    except requests.exceptions.ConnectTimeout:
        logger.warning("connection timed out to eplay.com. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to Eplay")
    return isOnline, title, thumbUrl, icon