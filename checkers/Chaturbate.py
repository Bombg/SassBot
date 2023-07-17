import time
from selenium.webdriver.common.by import By
import requests
from Constants import Constants
import json.decoder 

def isModelOnline(cbApiUrl):
    isOnline = False
    onlineModels = requests.get(cbApiUrl)
    time.sleep(3)
    try:
        results = onlineModels.json()["results"]
        title = "placeholder cb title"
        thumbUrl = ""
        icon = 'images/errIcon.png'
        for result in results:
            if result['username'] == Constants.cbUserName:
                isOnline = True
                title = result['room_subject']
                thumbUrl = result['image_url'] + "?" + str(int(time.time()))
    except json.decoder.JSONDecodeError:
        print("cb api didn't respond")
    return isOnline, title, thumbUrl, icon
