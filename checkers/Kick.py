import time
from SeleniumDriverCreator import SeleniumDriverCreator
import json

def isModelOnline(kickUserName):
    isOnline = False
    title = "place holder kick title, this should never show up unless coder fucked up"
    thumbUrl = ""
    icon = 'images/errIcon.png'
    apiUrl = f"https://kick.com/api/v1/channels/{kickUserName}"
    driverCreator = SeleniumDriverCreator()
    driver = driverCreator.createDriver()
    driver.get(apiUrl)
    time.sleep(3)
    content = driver.page_source.split('<body>')
    if len(content) < 2:
        print("error with kick checker. user is banned or wrong username supplied")
    else:
        jsonText = content[1].split('</body></html>')
        results = json.loads(jsonText[0])
        if results['livestream']:
            isOnline = True
            title = results['livestream']['session_title']
            thumbUrl = results['livestream']['thumbnail']['url']+ "?" + str(int(time.time()))
            icon = results['user']['profile_pic']
    return isOnline, title, thumbUrl, icon
