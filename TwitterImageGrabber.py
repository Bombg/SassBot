from SeleniumDriverCreator import SeleniumDriverCreator
from selenium.webdriver.common.by import By
import time
from Constants import Constants
import re
from Database import Database



def getImage():
    driverCreator = SeleniumDriverCreator()
    driver = driverCreator.createDriver()
    driver.get(Constants.twitterUrl)
    time.sleep(8)
    driver.get_screenshot_as_file("twitterShot.png")
    element = driver.find_elements(By.CLASS_NAME, 'css-9pa8cd')
    if len(element) > 0:
        reString = r'^https:\/\/pbs.twimg.com\/media\/.+small$'
        images = []
        for ele in element:
            if re.search(reString,ele.get_attribute('src')):
                images.append(ele.get_attribute('src'))
        imageSrc = getTwImgDb(images)
    else:
        imageSrc = 'images/twitErrImg.jpg'
    driver.quit()
    return imageSrc

def getTwImgDb(images):
    db = Database()
    twImgList, twImgQue = db.getTwImgStuff()
    if not twImgList:
        db.setTwImgList(images)
        db.setTwImgQueue(images)
        twImgList = images
        twImgQue = images
    elif images[0] not in twImgList:
        twImgList.insert(0, images[0])
        db.setTwImgList(twImgList)
        twImgQue.insert(0,images[0])
    elif not twImgQue:
        twImgQue = twImgList
    imageSrc = twImgQue.pop(0)
    db.setTwImgQueue(twImgQue)
    return imageSrc