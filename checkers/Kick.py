import asyncio
import json
import utils.NoDriverBrowserCreator as ndb
import globals
from DefaultConstants import Settings as Settings
import logging
from utils.StaticMethods import GetThumbnail
import requests
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.exceptions import InvalidSignature
import base64
import tls_client

baseSettings = Settings()
logger = logging.getLogger(__name__)
logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)

async def isModelOnline(kickUserName):
    isOnline, title, tempThumbUrl, icon = setDefaultStreamValues()
    apiUrl = f"https://kick.com/api/v1/channels/{kickUserName}"
    try:
        apiJson = GetIntApiJsonTls(apiUrl)
        if apiJson:
            isOnline, title, tempThumbUrl, icon = getStreamInfo(apiJson)
        else:
            logger.warning("error with kick checker. user is banned,wrong username supplied, or cloudflare bot detection")
    except Exception as e:
        logger.warning(f"error getting browser for Kick: {e}")
        globals.browserOpen = False
    thumbUrl = GetThumbnail(tempThumbUrl, baseSettings.kickThumbnail)
    return isOnline, title, thumbUrl, icon

async def GetNdJson(apiUrl):
    results = ""
    browser = await ndb.GetBrowser(proxy=baseSettings.KICK_PROXY)
    await asyncio.sleep(1*baseSettings.NODRIVER_WAIT_MULTIPLIER)
    page = await browser.get(apiUrl)
    await asyncio.sleep(1*baseSettings.NODRIVER_WAIT_MULTIPLIER)
    await page.save_screenshot("KickScreenshot.jpg")
    content = await page.get_content()
    content = content.split('<body>')
    await ndb.CloseNDBrowser(browser,page)
    if len(content) >= 2:
        jsonText = content[1].split('</body></html>')
        results = json.loads(jsonText[0])
    return results

def setDefaultStreamValues():
    isOnline = False
    title = "place holder kick title, this should never show up unless coder fucked up"
    thumbUrl = ""
    icon = baseSettings.defaultIcon
    return isOnline, title, thumbUrl, icon

def getStreamInfo(results):
    isOnline, title, thumbUrl, icon = setDefaultStreamValues()
    try:
        if 'livestream' in results and results['livestream']:
            title = results['livestream']['session_title']
            title = title.replace("&amp;","&")
            title = title.replace("&lt;", "<")
            thumbUrl = results['livestream']['thumbnail']['url']#+ "#" + str(int(time.time()))
            icon = results['user']['profile_pic']
            isOnline = True
    except json.decoder.JSONDecodeError:
        logger.warning("no json at kick api, bot detection site down, or cloudflare bot detection")
    return isOnline,title,thumbUrl,icon

def isModelOnlineAPI(kickUserName):
    apiResponse = getChannelInfoResponse([kickUserName])
    isOnline, title, icon, thumbUrl = getApiStreamingVals(kickUserName, apiResponse)

    return isOnline, title, thumbUrl, icon

def getChannelInfoResponse(kickUserNames:list):
    apiHeaders={"Authorization": getAccessToken(),"Accept":'application/json'}
    apiUrl = "https://api.kick.com/public/v1/channels"
    for i in range(len(kickUserNames)):
        kickUserNames[i] = kickUserNames[i].lower()
        kickUserNames[i] = kickUserNames[i].replace("_", "-")
    params = {"slug":[kickUserNames]}
    apiResponse = requests.get(apiUrl, headers=apiHeaders, params=params)
    if apiResponse.status_code == 401:
        logger.debug("401 w/kick attempting to get new access code")
        globals.kickAccessToken = None
        apiHeaders={"Authorization": getAccessToken(),"Accept":'application/json'}
        apiResponse = requests.get(apiUrl, headers=apiHeaders, params=params)
    return apiResponse

def getApiStreamingVals(kickUserName:str, apiResponse: requests.Response):
    apiData = apiResponse.json()
    isOnline, title, tempThumbUrl, icon = setDefaultStreamValues()
    if apiData:
        userId = apiData["data"][0]["broadcaster_user_id"]
        isOnline = apiData["data"][0]["stream"]["is_live"]
        tempThumbUrl = apiData["data"][0]["stream"]["thumbnail"]
        title = apiData["data"][0]["stream_title"]
        thumbUrl = GetThumbnail(tempThumbUrl, baseSettings.kickThumbnail)
        if kickUserName.lower() in globals.kickProfilePics:
            icon = globals.kickProfilePics[kickUserName.lower()]
        if kickUserName not in globals.kickUserIds:
            globals.kickUserIds[kickUserName] = userId
            subscribeWebhooks(globals.kickUserIds[kickUserName], "livestream.status.updated")
        logger.debug(apiData)
    else:
        logger.warning("Kick API: Failed to get data. status code:" + apiResponse.status_code)
    return isOnline,title,icon,thumbUrl

def getAccessToken():
    if not globals.kickAccessToken:
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        authorizationUrl = 'https://id.kick.com/oauth/token'
        tokenJson = {
                    "grant_type":"client_credentials",
                    "client_id": baseSettings.kickClientId,
                    "client_secret":baseSettings.kickClientSecret
        }
        response = requests.post(authorizationUrl, headers=headers, data=tokenJson)
        if response.status_code == 200:
            data = response.json()
            accessToken = data["access_token"]
            #expiresIn = data["expires_in"]
            tokenType = data["token_type"]
            globals.kickAccessToken = tokenType + " " + accessToken
        else:
            logger.warning(str(response.status_code) + " Failed to get access token from kick")
    return globals.kickAccessToken

def subscribeWebhooks(kickUserId, event):
    webResponse = postWebhooks(kickUserId, event)
    if webResponse.status_code == 200:
        logger.debug("Webhook " + event + " subscribed for " + str(kickUserId))
        logger.debug(webResponse.json())
        globals.kickEventIds.append(webResponse.json()["data"][0]["subscription_id"])
    else:
        logger.warning(str(webResponse.status_code) + " Failed to subscribe to webhooks")

def postWebhooks(kickUserId, event):
    webHeaders={"Authorization":getAccessToken(),"Content-Type":"application/json"}
    webhookReqUrl = "https://api.kick.com/public/v1/events/subscriptions"
    webData=json.dumps({
                        "broadcaster_user_id": kickUserId,
                        "events": [
                            {
                                "name": event,
                                "version": 1
                            }
                        ],
                        "method": "webhook"
    })
    webResponse = requests.post(webhookReqUrl,headers = webHeaders,data=webData)
    if webResponse.status_code == 401:
        logger.debug("401 w/kick attempting to get new access code")
        globals.kickAccessToken = None
        webHeaders={"Authorization":getAccessToken(),"Content-Type":"application/json"}
        webResponse = requests.post(webhookReqUrl,headers = webHeaders,data=webData)
    return webResponse

def deleteWebhookSubs(eventSubs: list):
    webHeaders={"Authorization":getAccessToken(),"Content-Type":"application/json"}
    webhookReqUrl = "https://api.kick.com/public/v1/events/subscriptions"
    params={"id": eventSubs}
    webResponse = requests.delete(webhookReqUrl,headers = webHeaders,params=params)
    if webResponse.status_code == 401:
        logger.debug("401 w/kick attempting to get new access code")
        globals.kickAccessToken = None
        webHeaders={"Authorization":getAccessToken(),"Content-Type":"application/json"}
        webResponse = requests.delete(webhookReqUrl,headers = webHeaders,params=params)
    if webResponse.status_code == 204:
        logger.debug("Successfully deleted kick event subs")
    else:
        logger.warning(str(webResponse.status_code) + " Couldn't delete kick event subs")

def GetWebhookSubs()-> dict:
    respJson = None
    webHeaders={"Authorization":getAccessToken(),"Content-Type":"application/json"}
    webhookReqUrl = "https://api.kick.com/public/v1/events/subscriptions"
    webResponse = requests.get(webhookReqUrl,headers = webHeaders)
    if webResponse.status_code == 401:
        logger.debug("401 w/kick attempting to get new access code")
        webHeaders={"Authorization":getAccessToken(),"Content-Type":"application/json"}
        webResponse = requests.get(webhookReqUrl,headers = webHeaders)
    if webResponse.status_code == 200:
        respJson = webResponse.json()
        logger.debug(webResponse.json())
    else:
        logger.warning(str(webResponse.status_code) + " error getting webhook sub list")
    return respJson

def DeleteAllWebhooks():
    if not baseSettings.kickClientId or not baseSettings.kickClientSecret: 
        return
    subs = GetWebhookSubs()
    if subs and 'data' in subs:
        subIds = []

        for sub in subs['data']:
            subIds.append(sub['id'])
        deleteWebhookSubs(subIds)

def verifyWebhook(headers, body:bytes):
    publicKey = getKickPublicKey()
    messageId = headers['kick-event-message-id']
    timestamp = headers['kick-event-message-timestamp']
    messageToVerify = f"{messageId}.{timestamp}.{body}".encode('utf-8')
    signature_b64 = headers['kick-event-signature'].encode('utf-8')
    isValid = verifySignature(
            publicKey,
            messageToVerify,
            signature_b64
        )
    return isValid

def verifySignature(publicKey: rsa.RSAPublicKey, message: bytes, signature_b64: bytes) -> bool:
    try:
        signature = base64.b64decode(signature_b64)
        publicKey.verify(
            signature,
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except (ValueError, TypeError) as e:
        logger.warning(f"Error decoding kick signature: {e}")
        return False
    
def getPublicKey()->bytes:
    if not globals.kickPublicKey:
        publicKeyUrl = 'https://api.kick.com/public/v1/public-key'
        request = requests.get(publicKeyUrl)
        if  request.status_code == 200:
            publicKey = request.json()['data']['public_key']
        else:
            logger.warning(str(request.status_code) + " error getting kick public key")
        globals.kickPublicKey = publicKey.encode('utf-8')
    return globals.kickPublicKey

def getKickPublicKey()-> rsa.RSAPublicKey:
    publicKey = getPublicKey()
    publicKey = serialization.load_pem_public_key(publicKey)
    return publicKey

def GetUserInfoFromToken(token:str):
    apiHeaders={"Authorization": token,"Accept":'application/json'}
    apiUrl = "https://api.kick.com/public/v1/users"
    #params = {"id":""}
    apiResponse = requests.get(apiUrl, headers=apiHeaders)
    if apiResponse.status_code == 401:
        logger.debug("401 w/kick attempting to get new access code")
        globals.kickAccessToken = None
        apiHeaders={"Authorization": getAccessToken(),"Accept":'application/json'}
        apiResponse = requests.get(apiUrl, headers=apiHeaders)
    return apiResponse

def GetIntApiJsonTls(apiUrl:str) -> json:
    headers = {
    'Origin': 'https://kick.com',
    'Cache-Control': 'no-cache',
    'Accept-Language': 'en-GB,en;q=0.9,af-ZA;q=0.8,af;q=0.7,en-US;q=0.6',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    }
    r = tls_client.Session(client_identifier="chrome_120", random_tls_extension_order=True)
    r.headers = headers 
    url = apiUrl
    r.headers["X-CLIENT-TOKEN"] = "e1393935a959b4020a4491574f6490129f678acdaa92760471263db43487f823"
    response = r.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None