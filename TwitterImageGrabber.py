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
    time.sleep(15)
    checkForAdultButton(driver)
    driver.get_screenshot_as_file("twitterShot.png")
    element = driver.find_elements(By.TAG_NAME, 'img')
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
            print("twitter image grabber isn't working for some reason. No images in element. All models images may be marked as 18+.")
    else:
        imageSrc = 'images/twitErrImg.jpg'
        print("twitter image grabber isn't working for some reason. No elements.")
    driver.quit()
    return imageSrc

def checkForAdultButton(driver):
    button = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div[2]/div/div[3]")
    if len(button) > 0:
        button[0].click()
        time.sleep(10)

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