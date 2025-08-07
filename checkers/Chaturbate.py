import time
import requests
from DefaultConstants import Settings as Settings
import json.decoder 
import logging
from utils.StaticMethods import GetThumbnail

baseSettings = Settings()
logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

def isModelOnline(cbUserName):
    isOnline = False
    title = "placeholder cb title"
    tempThumbUrl = ""
    icon = baseSettings.defaultIcon
    try:
        onlineModels = requests.get(baseSettings.cbApiUrl + f"&limit={baseSettings.cbJsonLimit}")
        time.sleep(3)
        try:
            results = onlineModels.json()["results"]
            count = onlineModels.json()['count']
            iterations = 1
            tempLimit = 0
            while count > tempLimit and not isOnline:
                tempLimit = baseSettings.cbJsonLimit * iterations
                for result in results:
                    if result['username'] == cbUserName:
                        isOnline = True
                        title = result['room_subject']
                        tempThumbUrl = result['image_url'] + "?" + str(int(time.time()))
                        break
                onlineModels = requests.get(baseSettings.cbApiUrl + f"&offset={tempLimit}")
                time.sleep(3)
                results = onlineModels.json()["results"]
                count = onlineModels.json()['count']
                iterations = iterations + 1
        except json.decoder.JSONDecodeError:
            logger.warning("cb api didn't respond")
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        logger.warning("connection timed out or aborted with Chaturbate. Bot detection or rate limited?")
    except requests.exceptions.SSLError:
        logger.warning("SSL Error when attempting to connect to Chaturbate")
    thumbUrl = GetThumbnail(tempThumbUrl, baseSettings.cbThumbnail)
    return isOnline, title, thumbUrl, icon
