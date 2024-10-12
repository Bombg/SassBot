import requests
import json
import json.decoder 
import time
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
from utils.NoDriverBrowserCreator import getUserAgent
import logging
from utils.StaticMethods import GetThumbnail

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

def isModelOnline(cam4UserName):
    title = Constants.cam4DefaultTitle
    tempThumbUrl = ""
    isOnline = False
    icon = Constants.defaultIcon
    agent = getUserAgent()
    try:
        headers = {"User-Agent": agent}
        results = requests.get(f"https://www.cam4.com/rest/v1.0/search/performer/{cam4UserName}", headers=headers)
        time.sleep(1)
        try:
            cam4Json = results.json()
            if cam4Json['online']:
                isOnline = True
                icon = cam4Json['profileImageUrl']
        except json.decoder.JSONDecodeError:
            logger.warning("cam4 api didn't respond?")
    except requests.exceptions.ConnectTimeout:
        logger.warning("connection timed out to cam4 api. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to Cam4")
    thumbUrl = GetThumbnail(tempThumbUrl, Constants.cam4Thumbnail)
    return isOnline, title, thumbUrl, icon