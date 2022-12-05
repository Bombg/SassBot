import asyncio
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator

class OnlyCas:
    def __init__(self):
        self.CAS_ONLY_URL = "https://onlyfans.com/badkittycass"

    async def isCassOnline(self):
        driverCreator = SeleniumDriverCreator()
        driver = driverCreator.createDriver()
        driver.get(self.CAS_ONLY_URL)
        await asyncio.sleep(10)
        online = driver.find_elements(By.XPATH, '/html/body/div/div[2]/main/div[1]/div[1]/div/div[2]/div/div[2]/div[1]/a/span')
        driver.quit()
        isOnline = False
        if len(online) > 0:
            isOnline = True

        return isOnline
