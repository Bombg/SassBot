import asyncio
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator

class ChaturCas:
    def __init__(self):
        self.CAS_CHATUR_URL = "https://chaturbate.com/badkittycass/"

    async def isCassOnline(self):
        driverCreator = SeleniumDriverCreator()
        driver = driverCreator.createDriver()
        driver.get(self.CAS_CHATUR_URL)
        await asyncio.sleep(5)
        online = driver.find_element(By.XPATH, '/html/body').text
        driver.quit()
        isOnline = False
        if 'offline' not in online:
            isOnline = True

        return isOnline


