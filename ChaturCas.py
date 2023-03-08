import asyncio
from SeleniumWireDriverCreator import SeleniumWireDriverCreator
import re

class ChaturCas:
    def __init__(self):
        self.CAS_CHATUR_URL = "https://chaturbate.com/badkittycass/"

    async def isCassOnline(self):
        ROOT_M3U8_RE = "https://.+\.m3u8"
        m3Match = re.compile(ROOT_M3U8_RE)
        driverCreator = SeleniumWireDriverCreator()
        driver = driverCreator.createDriver()
        driver.get(self.CAS_CHATUR_URL)
        m3List = []
        await asyncio.sleep(10)
        for netReq in driver.requests:
            if m3Match.match(netReq.url):
                m3List.append(netReq.url)
        driver.close()
        isOnline = False
        if len(m3List) > 0:
            isOnline = True

        return isOnline

# async def test():
#     chat = ChaturCas()
#     task = asyncio.create_task(chat.isCassOnline())
#     isOnline = await task
#     print(isOnline)

# task = asyncio.run(test())

