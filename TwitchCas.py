import requests
import time

class TwitchCas:

    def __init__(self):
        self.channelName = 'kitty_goes_mreow'
        
    # def isCassOnline(self):
    #     online = False
    #     contents = requests.get('https://www.twitch.tv/' + self.channelName).content.decode('utf-8')

    #     if 'isLiveBroadcast' in contents: 
    #         print(self.channelName + ' is live on twitch')
    #         online = True
    #     else:
    #         print(self.channelName + ' is not live on twitch')

    #     return online

    def isCassOnline(self):
        url = "https://gql.twitch.tv/gql"
        query = "query {\n  user(login: \""+ self.channelName +"\") {\n    stream {\n      id\n    }\n  }\n}"
        try:
            return True if requests.request("POST", url, json={"query": query, "variables": {}}, headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"}).json()["data"]["user"]["stream"] else False
        except(TypeError):
            return False
