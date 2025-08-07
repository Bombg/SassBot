import time
import requests
from DefaultConstants import Settings as Settings
from bs4 import BeautifulSoup
import logging
from utils.StaticMethods import GetThumbnail
from utils.StaticMethods import GetProxies

baseSettings = Settings()
logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

def isModelOnline(mfcUserName):
    isOnline = False
    title = baseSettings.mfcDefaultTitle
    tempThumbUrl = ""
    icon = baseSettings.defaultIcon
    try:
        if baseSettings.MFC_PROXY:
            request = requests.get(f"https://share.myfreecams.com/{mfcUserName}", proxies=GetProxies(baseSettings.MFC_PROXY))
        else:
            request = requests.get(f"https://share.myfreecams.com/{mfcUserName}")
        time.sleep(1)
        soup = BeautifulSoup(request.content, "html.parser")
        vidPreview = soup.find(class_='campreview d-none')
        if vidPreview:
            isOnline = True
            icon = soup.find(class_='avatar online').find("img")['src'] if soup.find(class_='avatar online') else soup.find(class_='avatar').find("img")['src']
    except requests.exceptions.ConnectTimeout:
        logger.warning("connection timed out to share.myfreecams.com. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to MyFreeCams")
    thumbUrl = GetThumbnail(tempThumbUrl, baseSettings.mfcThumbnail)
    return isOnline, title, thumbUrl, icon