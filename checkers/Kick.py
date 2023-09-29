import time
from SeleniumDriverCreator import SeleniumDriverCreator
import json
import StaticMethods

def isModelOnline(kickUserName):
    isOnline, title, thumbUrl, icon = setDefaultStreamValues()
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
        isOnline, title, thumbUrl, icon = getStreamInfo(jsonText)
    return isOnline, title, thumbUrl, icon

def setDefaultStreamValues():
    isOnline = False
    title = "place holder kick title, this should never show up unless coder fucked up"
    thumbUrl = ""
    icon = 'images/errIcon.png'
    return isOnline, title, thumbUrl, icon

def getStreamInfo(jsonText):
    isOnline, title, thumbUrl, icon = setDefaultStreamValues()
    try:
        results = json.loads(jsonText[0])
        if results['livestream']:
            title = results['livestream']['session_title']
            title = title.replace("&amp;","&")
            thumbUrl = results['livestream']['thumbnail']['url']+ "?" + str(int(time.time()))
            icon = results['user']['profile_pic']
            isOnline = True
    except json.decoder.JSONDecodeError:
        print("no json at kick api, bot detection or site down?")
    return isOnline,title,thumbUrl,icon
