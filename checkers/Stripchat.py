import requests
import json
import time
from Constants import Constants

def isModelOnline(scUserName):
    title = Constants.scDefaultTitle
    thumbUrl = ''
    isOnline = False
    icon = 'images/errIcon.png'
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0"}
    scJson = requests.get(f'https://stripchat.com/api/vr/v2/models/username/{scUserName}', headers=headers)
    time.sleep(1)
    if scJson.status_code == 200:
        try:
            scJson = scJson.json()
            isOnline = True if scJson['model']['status']  != 'off' else False
            icon = scJson['model']['avatarUrl']
            title = scJson['goal']['description'] if scJson['goal']['description'] else Constants.scDefaultTitle
            thumbUrl = scJson['model']['previewUrl']
        except json.decoder.JSONDecodeError:
            pass
    return isOnline, title, thumbUrl, icon