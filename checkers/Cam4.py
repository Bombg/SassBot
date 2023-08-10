import requests
import json
import json.decoder 
import time
from Constants import Constants

def isModelOnline(cam4UserName):
    title = Constants.cam4DefaultTitle
    thumbUrl = ''
    isOnline = False
    icon = 'images/errIcon.png'
    results = requests.get(f"https://www.cam4.com/rest/v1.0/search/performer/{cam4UserName}")
    time.sleep(1)
    try:
        cam4Json = results.json()
        if cam4Json['online']:
            isOnline = True
            icon = cam4Json['profileImageUrl']
    except json.decoder.JSONDecodeError:
        print("cam4 api didn't respond?")
    return isOnline, title, thumbUrl, icon