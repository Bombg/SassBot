from SeleniumDriverCreator import SeleniumDriverCreator
from selenium.webdriver.common.by import By
import asyncio
from Constants import Constants

class TwitterImageGrabber:

    def __init__(self) -> None:
        self.twitterUrl = Constants.twitterUrl

    async def getImage(self):
        driverCreator = SeleniumDriverCreator()
        driver = driverCreator.createDriver()
        driver.get(self.twitterUrl)
        await asyncio.sleep(8)
        driver.get_screenshot_as_file("twitterShot.png")
        element = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div[3]/div/div/div/div/div/div/a/div/div[2]/div/img')
        if len(element) > 0:
            imageSrc = element[0].get_attribute('src')
        else:
            imageSrc = 'plugins/avatars/missCass.png'
        driver.quit()
        return imageSrc