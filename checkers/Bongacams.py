import requests
import time
from bs4 import BeautifulSoup
import json

def isModelOnlineAlt(bcUserName):
    title = "placeholder bc title"
    thumbUrl = ''
    isOnline = False
    icon = 'images/errIcon.png'
    page = requests.get(f'https://bongacams.com/{bcUserName}')
    time.sleep(1)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        bcJson = []
        roomJsons = soup.find_all("script", type="application/json")
        for roomJson in roomJsons:
            if 'chatTopicOptions' in roomJson.text:
                bcJson = json.loads(roomJson.text)
                break
        if bcJson: 
            if bcJson["chatTopicOptions"]["currentTopic"]:
                title = bcJson["chatTopicOptions"]["currentTopic"]
                title = title.replace('\u200b', '')
                title = title.replace('\r', '')
                title = title.replace('\n', '')
            icon = bcJson['chatHeaderOptions']['profileImage']
            isOnline = not bcJson['chatShowStatusOptions']['isOffline']
            thumbUrl = bcJson['miniProfile']['albums']['albums'][0]['thumbImage']['src']
    return isOnline, title, thumbUrl, icon

# def isModelOnline(bcUserName):
#     isOnline = False
#     title = "placeholder bonga title"
#     thumbUrl = ""
#     icon = 'images/errIcon.png'
#     headers = {
#             "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0",
#             'Content-Type': 'application/x-www-form-urlencoded',
#             'Referer': 'https://de.bongacams.net/' + bcUserName,
#             'Accept': 'application/json, text/javascript, */*; q=0.01',
#             'X-Requested-With': 'XMLHttpRequest'
#         }
#     data = 'method=getRoomData&args%5B%5D=' + bcUserName + '&args%5B%5D=false'
#     req = requests.post('https://de.bongacams.net/tools/amf.php', data=data, headers=headers)
#     time.sleep(1)
#     if req.status_code == 200:
#         roomJson = req.json()
#         #print(roomJson)
#         if 'videoServerUrl' in roomJson['localData']:
#             bcUserName = roomJson['performerData']['username']
#             playlist = "https:" + roomJson['localData']['videoServerUrl'] + "/hls/stream_" + bcUserName + "/playlist.m3u8"
#             reqPl = requests.get(playlist)
#             print(reqPl.text)
#             if "#EXTM3U" in reqPl.text:
#                 isOnline = True
#     return isOnline, title, thumbUrl, icon


    