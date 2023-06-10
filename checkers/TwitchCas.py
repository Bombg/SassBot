import requests

def isCassOnline(channelName):
    url = "https://gql.twitch.tv/gql"
    query = "query {\n  user(login: \""+ channelName +"\") {\n    stream {\n      id\n    }\n  }\n}"
    title = "placeholder twitch title"
    isOnline = False
    try:
        if requests.request("POST", url, json={"query": query, "variables": {}}, headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"}).json()["data"]["user"]["stream"]:
            isOnline = True
        return isOnline, title
    except(TypeError):
        return isOnline, title
