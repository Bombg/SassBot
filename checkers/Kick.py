import asyncio
import nodriver as uc
import json
import time
import utils.NoDriverBrowserCreator as ndb
import globals
try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
import logging
from utils.StaticMethods import GetThumbnail
import requests
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.exceptions import InvalidSignature
import base64

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)

async def isModelOnline(kickUserName):
    isOnline, title, tempThumbUrl, icon = setDefaultStreamValues()
    apiUrl = f"https://kick.com/api/v1/channels/{kickUserName}"
    try:
        browser = await ndb.GetBrowser(proxy=Constants.KICK_PROXY)
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        page = await browser.get(apiUrl)
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        await page.save_screenshot("KickScreenshot.jpg")
        content = await page.get_content()
        content = content.split('<body>')
        if len(content) < 2:
            logger.warning("error with kick checker. user is banned,wrong username supplied, or cloudflare bot detection")
        else:
            jsonText = content[1].split('</body></html>')
            isOnline, title, tempThumbUrl, icon = getStreamInfo(jsonText)
        await page.close()
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        browser.stop()
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        globals.browserOpen = False
    except Exception as e:
        logger.warning(f"error getting browser for Kick: {e}")
        globals.browserOpen = False
    thumbUrl = GetThumbnail(tempThumbUrl, Constants.kickThumbnail)
    return isOnline, title, thumbUrl, icon

def setDefaultStreamValues():
    isOnline = False
    title = "place holder kick title, this should never show up unless coder fucked up"
    thumbUrl = ""
    icon = Constants.defaultIcon
    return isOnline, title, thumbUrl, icon

def getStreamInfo(jsonText):
    isOnline, title, thumbUrl, icon = setDefaultStreamValues()
    try:
        results = json.loads(jsonText[0])
        if results['livestream']:
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
    apiResponse = getChannelInfoResponse(kickUserName)
    isOnline, title, icon, thumbUrl = getApiStreamingVals(kickUserName, apiResponse)

    return isOnline, title, thumbUrl, icon

def getChannelInfoResponse(kickUserName):
    apiHeaders={"Authorization": getAccessToken(),"Accept":'application/json'}
    apiUrl = "https://api.kick.com/public/v1/channels"
    params = {"slug":[kickUserName]}
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
        thumbUrl = GetThumbnail(tempThumbUrl, Constants.kickThumbnail)
        if kickUserName.lower() in globals.kickProfilePics:
            icon = globals.kickProfilePics[kickUserName.lower()]
        if not kickUserName in globals.kickUserIds:
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
                    "client_id": Constants.kickClientId,
                    "client_secret":Constants.kickClientSecret
        }
        response = requests.post(authorizationUrl, headers=headers, data=tokenJson)
        data = response.json()
        if response.status_code == 200:
            accessToken = data["access_token"]
            expiresIn = data["expires_in"]
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