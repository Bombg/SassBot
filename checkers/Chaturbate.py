import time
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
        count = onlineModels.json()['count']
        iterations = 1
        tempLimit = 0
        while count > tempLimit and not isOnline:
            tempLimit = Constants.cbJsonLimit * iterations
            for result in results:
                if result['username'] == cbUserName:
                    isOnline = True
                    title = result['room_subject']
                    #thumbUrl = result['image_url'] + "?" + str(int(time.time()))
                    break
            onlineModels = requests.get(Constants.cbApiUrl + f"&offset={tempLimit}")
            time.sleep(3)
            results = onlineModels.json()["results"]
            count = onlineModels.json()['count']
            iterations = iterations + 1
        onlineModels.close()
    except json.decoder.JSONDecodeError:
        print("cb api didn't respond")
    return isOnline, title, thumbUrl, icon
