from SeleniumDriverCreator import SeleniumDriverCreator
from selenium.webdriver.common.by import By
import asyncio
from Constants import Constants
import re
import globals
from Database import Database

class TwitterImageGrabber:

    def __init__(self) -> None:
        self.twitterUrl = Constants.twitterUrl

    async def getImage(self):
        driverCreator = SeleniumDriverCreator()
        driver = driverCreator.createDriver()
        driver.get(self.twitterUrl)
        await asyncio.sleep(8)
        driver.get_screenshot_as_file("twitterShot.png")
        element = driver.find_elements(By.CLASS_NAME, 'css-9pa8cd')
        if len(element) > 0:
            reString = r'^https:\/\/pbs.twimg.com\/media\/.+small$'
            images = []
            for ele in element:
                if re.search(reString,ele.get_attribute('src')):
                    images.append(ele.get_attribute('src'))
            imageSrc = self.getTwImgDb(images)
        else:
            imageSrc = 'images/twitErrImg.jpg'
        driver.quit()
        return imageSrc

    def getTwImgDb(self, images):
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