import requests
import json
import time
from Constants import Constants
from NoDriverBrowserCreator import getUserAgent

def isModelOnline(scUserName):
    title = Constants.scDefaultTitle
    thumbUrl = ''
    isOnline = False
    icon = 'images/errIcon.png'
    agent = getUserAgent()
    headers = {"User-Agent": agent}
    page = requests.get(f'https://stripchat.com/api/vr/v2/models/username/{scUserName}', headers=headers)
    time.sleep(1)
    if page.status_code == 200:
        try:
            scJson = page.json()
            isOnline = True if scJson['model']['status']  != 'off' else False
            icon = scJson['model']['avatarUrl']
            title = scJson['goal']['description'] if scJson['goal']['description'] else Constants.scDefaultTitle
            thumbUrl = scJson['model']['previewUrl']
        except json.decoder.JSONDecodeError:
            pass
    page.close()
    return isOnline, title, thumbUrl, icon