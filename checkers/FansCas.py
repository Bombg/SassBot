import time
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator


def isCassOnline(CAS_FANS_URL):
    driverCreator = SeleniumDriverCreator()
    driver = driverCreator.createDriver()
    driver.get(CAS_FANS_URL)
    time.sleep(10)
    #driver.get_screenshot_as_file("Fansscreenshot.png")
    online = driver.find_elements(By.XPATH, '/html/body/app-root/div/div[1]/div/app-profile-route/div/div/div/div[1]/div[2]/div[1]/app-account-avatar/div')
    driver.quit()
    isOnline = False
    if len(online) > 0:
        isOnline = True
    return isOnline, "Naughty sleep stream? =)"
    
