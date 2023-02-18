import asyncio
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator
import time

class FansCas:
    def __init__(self):
        self.CAS_FANS_URL = "https://fansly.com/BadKittyCass"
        #https://fansly.com/live/user443986457938374656

    async def isCassOnline(self):
        driverCreator = SeleniumDriverCreator()
        driver = driverCreator.createDriver()
        driver.get(self.CAS_FANS_URL)
        await asyncio.sleep(10)
        #time.sleep(10)
        #driver.get_screenshot_as_file("Fansscreenshot.png")
        online = driver.find_elements(By.XPATH, '/html/body/app-root/div/div[1]/div/app-profile-route/div/div/div/div[1]/div[2]/div[1]/app-account-avatar/div')
        driver.quit()
        isOnline = False
        if len(online) > 0:
            isOnline = True

        return isOnline
    
