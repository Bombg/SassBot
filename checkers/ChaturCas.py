import asyncio
from selenium.webdriver.common.by import By
import requests

class ChaturCas:
    def __init__(self, chaturApiUrl):
        self.CAS_CHATUR_URL = chaturApiUrl

    async def isCassOnline(self):
        isOnline = False
        onlineModels = requests.get(self.CAS_CHATUR_URL)
        await asyncio.sleep(3)
        results = onlineModels.json()["results"]
        for result in results:
            #print(result['username'])
            if result['username'] == 'badkittycass':
                isOnline = True

        return isOnline

