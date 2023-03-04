import requests
import time
import asyncio
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator

class KickCass:
    def __init__(self):
        self.CAS_KICK_URL = 'https://kick.com/kittycass'
    def isCassOnline(self):
        driverCreator = SeleniumDriverCreator()
        driver = driverCreator.createDriver()
        driver.get(self.CAS_KICK_URL)
        #await asyncio.sleep(10)
        time.sleep(10)
        #driver.get_screenshot_as_file("Fansscreenshot.png")
        online = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/div/div[2]')
        driver.quit()
        isOnline = False
        if len(online) > 0:
            isOnline = True

        return isOnline
        

kick = KickCass()
online = kick.isCassOnline()
print(online)
