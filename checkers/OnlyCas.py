import time
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator

def isCassOnline(CAS_ONLY_URL):
    driverCreator = SeleniumDriverCreator()
    driver = driverCreator.createDriver()
    driver.get(CAS_ONLY_URL)
    time.sleep(10)
    online = driver.find_elements(By.XPATH, '/html/body/div/div[2]/main/div[1]/div[1]/div/div[2]/div/div[2]/div[1]/a/span')
    driver.quit()
    isOnline = False
    if len(online) > 0:
        isOnline = True
    return isOnline
