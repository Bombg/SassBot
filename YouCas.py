import requests
from bs4 import BeautifulSoup

class YouCas:
    def __init__(self):
        self.CAS_YT_URL = "https://www.youtube.com/c/@kitty_cass_/live"

    def isCassOnline(self):
        online = False
        page = requests.get(self.CAS_YT_URL, cookies={'CONSENT': 'YES+42'})
        soup = BeautifulSoup(page.content, "html.parser")
        live = soup.find("link", {"rel": "canonical"})
        if live: 
            #print("Cass is streaming on youtube")
            online = True
        #else:
            #print("Cass is not streaming on youtube")
        
        return online

