import asyncio
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator

class FansCas:
    def __init__(self):
        self.CAS_FANS_URL = "https://fansly.com/user443986457938374656"
        #https://fansly.com/live/user443986457938374656

    async def isCassOnline(self):
        driverCreator = SeleniumDriverCreator()
        driver = driverCreator.createDriver()
        driver.get(self.CAS_FANS_URL)
        await asyncio.sleep(10)
        online = driver.find_elements(By.XPATH, '/html/body/app-root/div/div[1]/div/app-profile-route/div/div/div/div[1]/div[5]/div')
        driver.quit()
        isOnline = False
        if len(online) > 0:
            isOnline = True

        return isOnline