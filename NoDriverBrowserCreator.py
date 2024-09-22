import requests
import random
import nodriver as uc
import psutil

def getUserAgent():
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

async def GetBrowser():
    # userAgent = getUserAgent()
    # browser_args=[f'user-agent={userAgent}','--mute-audio','--disable-3d-apis','--log-level=3','--disable-dev-shm-usage','--disable-gpu','--window-size=1920,1080','--start-maximized']
    try:
        browser = await uc.start(
        headless=False,
        sandbox=True,
    )
    except Exception as e:
        print(f"error creating browser in GetBrowser: {e}")
    return browser

def killBrowser(browser):
        try:
            process = psutil.Process(browser._process_pid)
            process.kill()  # Forcefully terminate the process.
        except psutil.NoSuchProcess:
            pass
        except Exception as e:
            print(f"Error terminating process {process.pid}: {e}")