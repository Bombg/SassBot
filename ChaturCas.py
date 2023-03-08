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
        button = driver.find_elements(By.XPATH, '//*[@id="close_entrance_terms"]')
        if len(button) > 0:
            button[0].click()
        await asyncio.sleep(3)
        online = driver.find_elements(By.XPATH, '//*[@id="vjs_video_3"]/div[4]/div[9]')
        driver.quit()
        isOnline = False
        if len(online) > 0:
            isOnline = True

        return isOnline


