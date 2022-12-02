import requests
from bs4 import BeautifulSoup

class YouCas:
    def __init__(self):
        self.CAS_YT_URL = "https://chaturbate.com/haruho/"

    def isCassOnline(self):
        online = True
        contents = requests.get(self.CAS_YT_URL).content.decode('utf-8')
        print(contents)
        #live = soup.find("link", {"rel": "canonical"})
        #if live: 
            #print("Cass is streaming on youtube")
            #online = True
        #else:
            #print("Cass is not streaming on youtube")
        
        return online


thingy = YouCas()
online = thingy.isCassOnline()