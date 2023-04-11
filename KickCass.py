import asyncio
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator

class KickCass:
    def __init__(self):
        self.CAS_KICK_URL = 'https://kick.com/kittycass'
    async def isCassOnline(self):
        driverCreator = SeleniumDriverCreator()
        driver = driverCreator.createDriver()
        isOnline = False
        offlineOwnerAvatar = []
        driver.get(self.CAS_KICK_URL)
        await asyncio.sleep(5)
        driver.get_screenshot_as_file("Kickscreenshot.png")
        offlineOwnerAvatar = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div')
        online = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/div/div[2]')
        if len(online) > 0:
            isOnline = True
        elif len(offlineOwnerAvatar) < 1:
            isOnline = 0
        return isOnline

async def test():
    kick = KickCass()
    task = asyncio.create_task(kick.isCassOnline())
    isOnline = await task
    print(isOnline)

task = asyncio.run(test())
