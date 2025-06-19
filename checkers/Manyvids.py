import requests
from bs4 import BeautifulSoup
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
from utils.StaticMethods import GetThumbnail
from utils.StaticMethods import GetProxies
import logging
import re
from utils.NoDriverBrowserCreator import getUserAgent

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

def isModelOnline(mvUserName):
    title = Constants.mvDefaultTitle
    tempThumbUrl = ''
    thumbUrl = ''
    isOnline = False
    icon = Constants.defaultIcon
    pageUrl = f"https://www.manyvids.com/live/cam/{mvUserName.lower()}"
    agent = getUserAgent()
    headers = {"User-Agent": agent}
    try:
        if Constants.MV_PROXY:
            page = requests.get(pageUrl, proxies=GetProxies(Constants.MV_PROXY), headers=headers)
        else:
            page = requests.get(pageUrl, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        onlineStatus = soup.find("div", {"class":"status_box__v1drl"})
        if onlineStatus:
            logger.debug(onlineStatus.text)
        else:
            logger.debug("no online status")
        if onlineStatus and (onlineStatus.text == "LIVE" or onlineStatus.text == "IN PRIVATE"):
            isOnline = True
            icon = GetIcon(soup, mvUserName)
            thumbUrl = GetThumbnail(tempThumbUrl, Constants.mvThumbnail)
    except requests.exceptions.ConnectionError as e:
        logger.warning(e)
    except requests.exceptions.ChunkedEncodingError as e:
        logger.warning(e)
    return isOnline, title, thumbUrl, icon

def GetIcon(soup:BeautifulSoup, mvUserName):
    icon = Constants.defaultIcon
    reString = r"https:\/\/cdn5\.manyvids\.com\/php_uploads\/profile\/" + mvUserName + r"\/image\/cropped-image_\d+.jpeg"
    icon = re.search(reString, soup.prettify())
    if icon:
        icon = icon.group()
    return icon
