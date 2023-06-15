import time
import cloudscraper

def isCassOnline(username):
    isOnline = False
    title = "place holder kick title, this should never show up unless coder fucked up"
    apiUrl = f"https://kick.com/api/v1/channels/{username}"
    scraper = cloudscraper.create_scraper()
    streamerJson = scraper.get(apiUrl)
    time.sleep(3)
    results = streamerJson.json()
    if results['livestream']:
        isOnline = True
        title = results['livestream']['session_title']
    return isOnline, title
