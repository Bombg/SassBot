import requests

def isCassOnline(channelName):
    url = "https://gql.twitch.tv/gql"
    query = "query {\n  user(login: \""+ channelName +"\") {\n    stream {\n      id\n    }\n  }\n}"
    title = "placeholder twitch title"
    thumbUrl = f'https://static-cdn.jtvnw.net/previews-ttv/live_user_{channelName}-1920x1080.jpg'
    isOnline = False
    icon = 'images/errIcon.png'
    req = requests.request("POST", url, json={"query": query, "variables": {}}, headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"})
    try:
        if req.json()["data"]["user"]["stream"]:
            isOnline = True
        return isOnline, title,thumbUrl, icon
    except(TypeError):
        return isOnline, title, thumbUrl, icon
