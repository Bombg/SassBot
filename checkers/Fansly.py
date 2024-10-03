import time
from selenium.webdriver.common.by import By
from SeleniumDriverCreator import SeleniumDriverCreator
from Constants import Constants
import StaticMethods


def isModelOnline(fansUserName):
    fansUrl = f"https://fansly.com/{fansUserName}"
    thumbUrl = ""
    icon = 'images/errIcon.png'
    isOnline = False
    title = Constants.fansDefaultTitle
    driverCreator = SeleniumDriverCreator()
    driver = driverCreator.createDriver(proxy=Constants.FANS_PROXY)
    driver.get(fansUrl)
    time.sleep(10)
    checkForEnterButton(driver)
    driver.get_screenshot_as_file("Fansscreenshot.png")
    online = driver.find_elements(By.XPATH, '/html/body/app-root/div/div[1]/div/app-profile-route/div/div/div/div[1]/div[2]/div[1]/app-account-avatar/div')
    iconEle = driver.find_elements(By.TAG_NAME, 'img')
    if len(iconEle) >= 5:
        byte = StaticMethods.get_file_content_chrome(driver, iconEle[4].get_attribute('src'))
        file = open("images/fansIcon.jpg", 'wb')
        file.write(byte)
        file.close()
        icon = "images/fansIcon.jpg"
    driver.quit()
    if len(online) > 0:
        isOnline = True
    return isOnline, title, thumbUrl, icon

def checkForEnterButton(driver):
    button = driver.find_elements(By.XPATH, "/html/body/app-root/div/div[3]/app-age-gate-modal/div/div/div[4]/div/div[2]")
    if len(button) > 0:
        button[0].click()
        time.sleep(10)


    
