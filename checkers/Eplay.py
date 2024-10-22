import time
import requests
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
from bs4 import BeautifulSoup
import json
import logging
from utils.StaticMethods import GetThumbnail
from utils.StaticMethods import GetProxies

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

def isModelOnline(epUserName):
    isOnline = False
    title = Constants.epDefaultTitle
    tempThumbUrl = ""
    icon = Constants.defaultIcon
    try:
        if Constants.EP_PROXY:
            request = requests.get(f"https://eplay.com/{epUserName}", proxies=GetProxies(Constants.EP_PROXY))
        else:
            request = requests.get(f"https://eplay.com/{epUserName}")
        time.sleep(1)
        soup = BeautifulSoup(request.content, "html.parser")
        profileJson = soup.find_all("script", type="application/json")
        profileJson = json.loads(profileJson[0].text)
        isOnline = profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["live"]
        title =  profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["title"]
        title = title.replace('\u200b', '')
        title = title.replace('\r', '')
        title = title.replace('\n', '')
        tempThumbUrl = profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["ss"] + "?" + str(int(time.time()))
        icon =  profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["avatar"]
    except requests.exceptions.ConnectTimeout:
        logger.warning("connection timed out to eplay.com. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to Eplay")
    thumbUrl = GetThumbnail(tempThumbUrl, Constants.epThumbnail)
    return isOnline, title, thumbUrl, icon