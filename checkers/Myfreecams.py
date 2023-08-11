import time
from selenium.webdriver.common.by import By
import requests
from Constants import Constants
from bs4 import BeautifulSoup

def isModelOnline(mfcUserName):
    isOnline = False
    title = "placeholder mfc title"
    thumbUrl = ""
    icon = 'images/errIcon.png'
    request = requests.get(f"https://share.myfreecams.com/{mfcUserName}")
    time.sleep(1)
    soup = BeautifulSoup(request.content, "html.parser")
    vidPreview = soup.find(class_='campreview-link')
    if vidPreview:
        isOnline = True
        icon = soup.find(class_='avatar online').find("img")['src'] if soup.find(class_='avatar online') else soup.find(class_='avatar').find("img")['src']
    return isOnline, title, thumbUrl, icon