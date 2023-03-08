import seleniumwire.undetected_chromedriver.v2 as uc

class SeleniumWireDriverCreator:
    def createDriverOptions(self):
        chrome_options = uc.ChromeOptions()
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

        return chrome_options

    def createDriver(self):
        chrome_options = self.createDriverOptions()
        driver = uc.Chrome(options=chrome_options)

        return driver