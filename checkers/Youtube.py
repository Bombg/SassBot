import requests
from bs4 import BeautifulSoup
import json

def isModelOnline(ytUrl):
    online = False
    title =  "placeholder youtube title"
    thumbUrl = ""
    icon = 'images/errIcon.png'
    page = requests.get(ytUrl, cookies={'CONSENT': 'YES+42'})
    soup = BeautifulSoup(page.content, "html.parser")
    live = soup.find("link", {"rel": "canonical"})
    scripts = soup.find_all('script')
    ytJson = str(scripts).split('var ytInitialPlayerResponse = ')
    ytJson2 = str(scripts).split('var ytInitialData = ')
    try:
        splitJson = str(ytJson[1]).split(";</script>")
        splitJson2 = str(ytJson2[1]).split(";</script>")
        iconJson = json.loads(splitJson2[0])
        compJson = json.loads(splitJson[0])
        status = compJson["playabilityStatus"]["status"]
        title = compJson["videoDetails"]['title']
        thumbUrl = compJson['videoDetails']['thumbnail']['thumbnails'][4]['url']
        icon = iconJson['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['thumbnail']['thumbnails'][0]['url']
        if live and status != "LIVE_STREAM_OFFLINE": 
            online = True
    except IndexError:
        pass    
    return online,title, thumbUrl, icon