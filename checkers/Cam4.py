import requests
import json
import json.decoder 
import time
from Constants import Constants
from NoDriverBrowserCreator import getUserAgent

def isModelOnline(cam4UserName):
    title = Constants.cam4DefaultTitle
    thumbUrl = ''
    isOnline = False
    icon = 'images/errIcon.png'
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
            results.close()
        except json.decoder.JSONDecodeError:
            print("cam4 api didn't respond?")
    except requests.exceptions.ConnectTimeout:
        print("connection timed out to cam4 api. Bot detection or rate limited?")
    return isOnline, title, thumbUrl, icon