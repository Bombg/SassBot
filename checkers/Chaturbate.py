import time
from selenium.webdriver.common.by import By
import requests
from Constants import Constants
import json.decoder 

def isModelOnline(cbUserName):
    isOnline = False
    title = "placeholder cb title"
    thumbUrl = ""
    icon = 'images/errIcon.png'
    onlineModels = requests.get(Constants.cbApiUrl)
    time.sleep(3)
    try:
        results = onlineModels.json()["results"]
        for result in results:
            if result['username'] == cbUserName:
                isOnline = True
                title = result['room_subject']
                thumbUrl = result['image_url'] + "?" + str(int(time.time()))
    except json.decoder.JSONDecodeError:
        print("cb api didn't respond")
    return isOnline, title, thumbUrl, icon
