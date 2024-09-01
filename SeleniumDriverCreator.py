from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import random
import platform
import re

class SeleniumDriverCreator:
    def createDriverOptions(self):
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--mute-audio")
        chromeOptions.add_argument("--disable-3d-apis")
        chromeOptions.add_argument('--log-level=3')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        chromeOptions.add_argument("--disable-gpu")
        chromeOptions.add_argument("--window-size=1920,1080")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument("--proxy-server='direct://'")
        chromeOptions.add_argument("--proxy-bypass-list=*")
        chromeOptions.add_argument("--start-maximized")
        chromeOptions.add_argument('--ignore-certificate-errors')
        userAgent = self.getUserAgent()
        chromeOptions.add_argument(f'user-agent={userAgent}')
        chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
        chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
        chromeOptions.add_experimental_option("useAutomationExtension", False)

        return chromeOptions

    def createDriver(self):
        chromeOptions = self.createDriverOptions()
        driver = webdriver.Chrome(options=chromeOptions)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver
    
    def getUserAgent(self):
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/127.0.2651.105"
        try:
            page = requests.get('https://jnrbsn.github.io/user-agents/user-agents.json')
            userAgentsJson = page.json()
            # osName = platform.system()
            # reString = f"^.+\\(.*{osName}.*\\).*Chrome.*$"
            # for agent in userAgentsJson:
            #     if re.search(reString, agent):
            #         userAgent = agent
            #         break
            userAgent = random.choice(userAgentsJson)
        except:
            print("Trouble getting user agent from jnrbsn's github. Using default")
        return userAgent
