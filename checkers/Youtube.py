import requests
from bs4 import BeautifulSoup
import json

def isModelOnline(ytUserName):
    ytUrl = f"https://www.youtube.com/@{ytUserName}/live"
    online = False
    title =  "placeholder youtube title"
    thumbUrl = ""
    icon = 'images/errIcon.png'
    page = requests.get(ytUrl, cookies={'CONSENT': 'YES+42'})
    soup = BeautifulSoup(page.content, "html.parser")
    live = soup.find("link", {"rel": "canonical"})
    scripts = soup.find_all('script')
    liveJson = getLiveJson(scripts)
    if liveJson:
        iconJson = getIconJson(scripts)
        status = liveJson["playabilityStatus"]["status"]
        title = liveJson["videoDetails"]['title']
        thumbUrl = liveJson['videoDetails']['thumbnail']['thumbnails'][4]['url']
        if live and status != "LIVE_STREAM_OFFLINE": 
            online = True
        if iconJson:
            icon = iconJson['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['thumbnail']['thumbnails'][0]['url']
        else:
            print("can't get yt icon")
    page.close()
    return online,title, thumbUrl, icon

def getIconJson(scripts):
    iconJson = 0
    try:
        ytJson2 = str(scripts).split('var ytInitialData = ')
        splitJson2 = str(ytJson2[1]).split(";</script>")
        iconJson = json.loads(splitJson2[0])
    except IndexError:
        pass
    return iconJson

def getLiveJson(scripts):
    liveJson = 0
    try:
        ytJson = str(scripts).split('var ytInitialPlayerResponse = ')
        splitJson = str(ytJson[1]).split(";</script>")
        liveJson = json.loads(splitJson[0])
    except IndexError:
        pass
    return liveJson