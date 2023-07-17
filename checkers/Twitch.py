import requests
import json
from bs4 import BeautifulSoup
import time
import StaticMethods

def isModelOnline(twitchChannelName):
    title = "placeholder twitch title"
    thumbUrl = ''
    isOnline = False
    icon = 'images/errIcon.png'
    page = requests.get(f'https://www.twitch.tv/{twitchChannelName}')
    time.sleep(1)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        firstSplit = soup.prettify().split('<script type=\"application/ld+json\">\n    [')
        jsonSplit = firstSplit[1].split(']\n   </script>')
        twitchJson = json.loads(jsonSplit[0])
        title = twitchJson['description']
        thumbnail = twitchJson['thumbnailUrl'][2]
        rerun = StaticMethods.isRerun(title)
        if not rerun:
            isOnline = twitchJson['publication']['isLiveBroadcast']
    except IndexError:
        pass
    
    return isOnline, title, thumbUrl, icon
