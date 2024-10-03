import time
import requests
from Constants import Constants
from bs4 import BeautifulSoup
import json

def isModelOnline(epUserName):
    isOnline = False
    title = Constants.epDefaultTitle
    thumbUrl = ""
    icon = 'images/errIcon.png'
    try:
        request = requests.get(f"https://eplay.com/{epUserName}")
        time.sleep(1)
        soup = BeautifulSoup(request.content, "html.parser")
        profileJson = soup.find_all("script", type="application/json")
        profileJson = json.loads(profileJson[0].text)
        isOnline = profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["live"]
        title =  profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["title"]
        thumbUrl = profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["ss"]
        icon =  profileJson["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["avatar"]
        request.close()
    except requests.exceptions.ConnectTimeout:
        print("connection timed out to eplay.com. Bot detection or rate limited?")
    return isOnline, title, thumbUrl, icon