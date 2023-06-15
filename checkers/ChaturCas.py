import time
from selenium.webdriver.common.by import By
import requests
from Constants import Constants

def isCassOnline(CAS_CHATUR_URL):
    isOnline = False
    onlineModels = requests.get(CAS_CHATUR_URL)
    time.sleep(3)
    results = onlineModels.json()["results"]
    title = "placeholder cb title"
    for result in results:
        #print(result['username'])
        if result['username'] == Constants.cbUserName:
            isOnline = True
            title = result['room_subject']
    return isOnline, title
