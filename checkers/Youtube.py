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
    try:
        splitJson = str(ytJson[1]).split(";</script>")
        compJson = json.loads(splitJson[0])
        status = compJson["playabilityStatus"]["status"]
        if live and status != "LIVE_STREAM_OFFLINE": 
            online = True
    except IndexError:
        pass    
    return online,title, thumbUrl, icon