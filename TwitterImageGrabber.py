from SeleniumDriverCreator import SeleniumDriverCreator
from selenium.webdriver.common.by import By
import asyncio
from Constants import Constants
import re
import globals

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
            reString = '^https:\/\/pbs.twimg.com\/media\/.+small$'
            images = []
            for ele in element:
                if re.search(reString,ele.get_attribute('src')):
                    images.append(ele.get_attribute('src'))
            if globals.twitImages == images:
                imageSrc = images[globals.twitCycle % len(images)]
                globals.twitCycle = globals.twitCycle + 1
            else:
                imageSrc = images[0]
                globals.twitImages = images
                globals.twitCycle = globals.twitCycle + 1
        else:
            imageSrc = 'images/twitErrImg.jpg'
        driver.quit()
        return imageSrc