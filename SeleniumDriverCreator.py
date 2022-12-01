from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SeleniumDriverCreator:
    def createDriverOptions(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--disable-3d-apis")
        chrome_options.add_argument('--log-level=3')

        return chrome_options

    def createDriver(self):
        chrome_options = self.createDriverOptions()
        driver = webdriver.Chrome(options=chrome_options)

        return driver