import asyncio
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator

class KickCass:
    def __init__(self,kickUrl):
        self.CAS_KICK_URL = kickUrl
    async def isCassOnline(self):
        driverCreator = SeleniumDriverCreator()
        driver = driverCreator.createDriver()
        isOnline = False
        offlineOwnerAvatar = []
        driver.get(self.CAS_KICK_URL)
        await asyncio.sleep(5)
        driver.get_screenshot_as_file("Kickscreenshot.png")
        button = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div[4]/button[2]')
        if len(button) > 0:
            button[0].click()
            offlineOwnerAvatar = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div')
            online = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/div/div[2]')
            driver.quit()
            if len(online) > 0:
                isOnline = True
            elif len(offlineOwnerAvatar) < 1:
                isOnline = 3
        else:
            print("didn't find kick button, super fail, fix me pls")
        return isOnline
