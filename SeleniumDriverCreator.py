from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
import platform
import re

class SeleniumDriverCreator:
    def createDriverOptions(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--disable-3d-apis")
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--ignore-certificate-errors')
        userAgent = self.getUserAgent()
        chrome_options.add_argument(f'user-agent={userAgent}')

        return chrome_options

    def createDriver(self):
        chrome_options = self.createDriverOptions()
        driver = webdriver.Chrome(options=chrome_options)

        return driver
    
    def getUserAgent(self):
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/127.0.2651.105"
        try:
            page = requests.get('https://jnrbsn.github.io/user-agents/user-agents.json')
            userAgentsJson = page.json()
            osName = platform.system()
            reString = f"^.+\\(.*{osName}.*\\).*Chrome.*$"
            for agent in userAgentsJson:
                if re.search(reString, agent):
                    userAgent = agent
                    break
        except:
            print("Trouble getting user agent from jnrbsn's github. Using default")
        return userAgent
