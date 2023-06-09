import asyncio
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator
from Constants import Constants
import time

def isCassOnline(url):
    driverCreator = SeleniumDriverCreator()
    driver = driverCreator.createDriver()
    isOnline = False
    title = Constants.streamerName + " is live on Kick!"
    offlineOwnerAvatar = []
    driver.get(url)
    time.sleep(5)
    driver.get_screenshot_as_file("Kickscreenshot.png")
    offlineOwnerAvatar = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div')
    online = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div[4]/button[2]')
    if len(online) > 0:
        isOnline = True
        titleX = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div[2]/span')
        if len(titleX) > 0:
            title = titleX[0].get_attribute("innerHTML")
            title = title.split("<!---->")[0]
    elif len(offlineOwnerAvatar) < 1:
        isOnline = 3
    driver.quit()
    return isOnline, title
