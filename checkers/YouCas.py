import requests
from bs4 import BeautifulSoup
import json

def isCassOnline(CAS_YT_URL):
    online = False
    title =  "placeholder youtube title"
    thumbUrl = ""
    page = requests.get(CAS_YT_URL, cookies={'CONSENT': 'YES+42'})
    soup = BeautifulSoup(page.content, "html.parser")
    live = soup.find("link", {"rel": "canonical"})
    scripts = soup.find_all('script')
    ytJson = str(scripts).split('var ytInitialPlayerResponse = ')
    splitJson = str(ytJson[1]).split(";</script>")
    compJson = json.loads(splitJson[0])
    status = compJson["playabilityStatus"]["status"]
    if live and status != "LIVE_STREAM_OFFLINE": 
        online = True    
    return online,title, thumbUrl