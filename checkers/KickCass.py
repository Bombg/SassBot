import time
from SeleniumDriverCreator import SeleniumDriverCreator
import json

def isCassOnline(username):
    isOnline = False
    title = "place holder kick title, this should never show up unless coder fucked up"
    thumbUrl = ""
    apiUrl = f"https://kick.com/api/v1/channels/{username}"

    driverCreator = SeleniumDriverCreator()
    driver = driverCreator.createDriver()
    driver.get(apiUrl)
    time.sleep(3)
    content = driver.page_source.split('<body>')
    jsonText = content[1].split('</body></html>')
    results = json.loads(jsonText[0])
    if results['livestream']:
        isOnline = True
        title = results['livestream']['session_title']
        thumbUrl = results['livestream']['thumbnail']['url']

    return isOnline, title, thumbUrl
