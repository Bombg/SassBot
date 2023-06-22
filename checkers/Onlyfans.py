import time
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator
from Constants import Constants
import re

def isModelOnline(ofUrl):
    title = Constants.ofDefaultTitle
    thumbUrl = ""
    icon = 'images/errIcon.png'
    reString = r'^https:\/\/.+avatar.jpg$'
    driverCreator = SeleniumDriverCreator()
    driver = driverCreator.createDriver()
    driver.get(ofUrl)
    time.sleep(10)
    online = driver.find_elements(By.XPATH, '/html/body/div/div[2]/main/div[1]/div[1]/div/div[2]/div/div[2]/div[1]/a/span')
    iconEle = driver.find_elements(By.TAG_NAME, 'img')
    if len(iconEle) > 0:
        for ele in iconEle:
            if re.search(reString, ele.get_attribute('src')):
                icon = ele.get_attribute('src')
                break
    driver.quit()
    isOnline = False
    if len(online) > 0:
        isOnline = True
    return isOnline, title, thumbUrl, icon
