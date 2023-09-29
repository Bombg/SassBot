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
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0"}
        results = requests.get(f"https://www.cam4.com/rest/v1.0/search/performer/{cam4UserName}", headers=headers)
        time.sleep(1)
        try:
            cam4Json = results.json()
            if cam4Json['online']:
                isOnline = True
                icon = cam4Json['profileImageUrl']
        except json.decoder.JSONDecodeError:
            print("cam4 api didn't respond?")
    except requests.exceptions.ConnectTimeout:
        print("connection timed out to cam4 api. Bot detection or rate limited?")
    return isOnline, title, thumbUrl, icon