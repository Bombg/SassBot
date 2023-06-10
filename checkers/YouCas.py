import requests
from bs4 import BeautifulSoup
import json

def isCassOnline(CAS_YT_URL):
    online = False
    page = requests.get(CAS_YT_URL, cookies={'CONSENT': 'YES+42'})
    soup = BeautifulSoup(page.content, "html.parser")
    live = soup.find("link", {"rel": "canonical"})
    scripts = soup.find_all('script')
    ytJson = str(scripts).split('var ytInitialPlayerResponse = ')
    # with open('jsonText', 'w', encoding="utf-8") as f:
    #     f.write(ytJson[1])
    splitJson = str(ytJson[1]).split(";</script>")
    compJson = json.loads(splitJson[0])
    status = compJson["playabilityStatus"]["status"]
    if live and status != "LIVE_STREAM_OFFLINE": 
        #print("Cass is streaming on youtube")
        online = True
    #else:
        #print("Cass is not streaming on youtube")
        
    return online, "placeholder youtube title"