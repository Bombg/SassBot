import requests
import time

class TwitchCas:

    def __init__(self, twitchChanName):
        self.channelName = twitchChanName
        
    def isCassOnline(self):
        url = "https://gql.twitch.tv/gql"
        query = "query {\n  user(login: \""+ self.channelName +"\") {\n    stream {\n      id\n    }\n  }\n}"
        try:
            return True if requests.request("POST", url, json={"query": query, "variables": {}}, headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"}).json()["data"]["user"]["stream"] else False
        except(TypeError):
            return False
