from SeleniumDriverCreator import SeleniumDriverCreator
from selenium.webdriver.common.by import By
import time
from Constants import Constants
import re
from Database import Database
import StaticMethods



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
        if len(images) > 0:
            imageSrc = getTwImgDb(images)
        else:
            imageSrc = 'images/twitErrImg.jpg'
            print("twitter image grabber isn't working for some reason. No images in element")
    else:
        imageSrc = 'images/twitErrImg.jpg'
        print("twitter image grabber isn't working for some reason. No elements")
    driver.quit()
    return imageSrc

def getTwImgDb(images):
    db = Database()
    twImgList, twImgQue, bannedList = db.getTwImgStuff()
    if not twImgList:
        db.setTwImgList(images)
        db.setTwImgQueue(images)
        twImgList = images
        twImgQue = images
    elif images[0] not in twImgList and images[0] not in bannedList:
        StaticMethods.pinImage(images[0],Constants.pinTimeLong)
        twImgList.insert(0, images[0])
        db.setTwImgList(twImgList)
    elif not twImgQue:
        twImgQue = twImgList
    url = StaticMethods.checkImagePin()
    if url:
        imageSrc = url
    else:
        imageSrc = twImgQue.pop(0)
        db.setTwImgQueue(twImgQue)
    return imageSrc