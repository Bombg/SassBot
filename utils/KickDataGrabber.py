try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
import logging
import utils.NoDriverBrowserCreator as ndb
import globals
import asyncio
import json
from utils.Database import Database
import datetime
from datetime import datetime as dt
from datetime import timedelta
from datetime import timezone
import hikari

logger = logging.getLogger(__name__)
logger.setLevel(Constants.SASSBOT_LOG_LEVEL)
#https://kick.com/{kickSlug}/clips/{clipId} 
async def CollectClipData(kickSlug:str, rest: hikari.impl.RESTClientImpl) -> None:
    db = Database()
    apiUrl = f"https://kick.com/api/v2/channels/{kickSlug}/clips"
    if globals.kickClipCursor:
        apiUrl = f"{apiUrl}?cursor={globals.kickClipCursor}"
    browser = await ndb.GetBrowser(proxy=Constants.KICK_PROXY)
    try:
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        page = await browser.get(apiUrl)
        await asyncio.sleep(1*Constants.NODRIVER_WAIT_MULTIPLIER)
        await page.save_screenshot("KickClipsScreenshot.jpg")
        content = await page.get_content()
        content = content.split('<body>')
        if len(content) < 2:
            logger.warning("error with clip checker. user is banned,wrong username supplied, or cloudflare bot detection")
        else:
            jsonText = content[1].split('</body></html>')
            results = json.loads(jsonText[0])
            if 'nextCursor' in results:
                globals.kickClipCursor = results['nextCursor']
                logger.debug(f"grabbing clip data from {apiUrl} and going again at cursor: {results['nextCursor']}")
            for clip in results['clips']:
                exeString = f'''SELECT clip_id FROM kick_clips WHERE clip_id='{clip['id']}' '''
                creationDate = dt.strptime(clip['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
                timeDiff = dt.now(timezone.utc) - creationDate
                daysClipLookBack = 30
                viewIncrease = 0
                if not db.isExists(exeString):
                    db.addKickClipToTable(clip['id'], clip['livestream_id'],clip['channel']['slug'], clip['creator']['slug'], clip['created_at'], clip['title'], clip['views'], clip['category']['slug'])
                    if timeDiff < timedelta(days=daysClipLookBack):
                        viewIncrease = clip['views']
                        globals.kickClipMostViewedUser[clip['creator']['slug']] = viewIncrease
                        if not clip['creator']['slug'] in globals.kickClipMostClips:
                            globals.kickClipMostClips[clip['creator']['slug']] = []
                        globals.kickClipMostClips[clip['creator']['slug']].append(clip['id'])
                elif timeDiff < timedelta(days=daysClipLookBack):
                    previousViews = db.getKickClipViews(clip['id'],clip['channel']['slug'])
                    viewIncrease = clip['views'] - previousViews
                    if not clip['creator']['slug'] in globals.kickClipMostViewedUser:
                        globals.kickClipMostViewedUser[clip['creator']['slug']] = 0
                    if not clip['creator']['slug'] in globals.kickClipMostClips:
                        globals.kickClipMostClips[clip['creator']['slug']] = []
                    if clip['id'] not in  globals.kickClipMostClips[clip['creator']['slug']]:
                        globals.kickClipMostClips[clip['creator']['slug']].append(clip['id'])
                    globals.kickClipMostViewedUser[clip['creator']['slug']] = globals.kickClipMostViewedUser[clip['creator']['slug']] + viewIncrease
                    db.updateKickClipViews(clip['id'],clip['views'])
                else:
                    globals.kickClipCursor = ""
                if viewIncrease > globals.kickClipMostViews:
                    globals.kickClipMostViews = viewIncrease
                    globals.kickClipMostViewsId = clip['id']
                    globals.kickClipMostViewsClipper = clip['creator']['slug']
                    globals.kickClipMostViewsTitle = clip['title']
            if not globals.kickClipCursor:
                await AnnounceWinnersHandleData(kickSlug, rest, db) 
        await ndb.CloseNDBrowser(browser, page)
    except Exception as e:
        logger.exception(e)
        globals.browserOpen = False

async def AnnounceWinnersHandleData(kickSlug: str, rest:hikari.impl.RESTClientImpl, db:Database):
    today = datetime.date.today()
    isoYear, isoWeek, isoDayOfWeek = today.isocalendar()
    mostViewedClipUrl = f'https://kick.com/{kickSlug}/clips/{globals.kickClipMostViewsId}'
    mostViewedUser, views = GetMostViewedClipper()
    mostClipper, numClips = GetMostClipper()
    messageContent=f"# Kick Clip Stats For Week {isoWeek} Of {isoYear}:\n" \
                    f"### Most Viewed Clipper:\n" \
                    f"- ** {mostViewedUser.capitalize()} ** with ** {views} ** total views across all their clips\n"\
                    f"### Most Prolific Clipper:\n" \
                    f"- ** {mostClipper.capitalize()} ** with ** {numClips} ** clips\n"\
                    f"## Most Viewed Clip:\n" \
                    f"- ** {globals.kickClipMostViewsTitle.capitalize()} ** \n" \
                    f"     - clipped by: ** {globals.kickClipMostViewsClipper.capitalize()} ** \n"\
                    f"     - ** {mostViewedClipUrl} **"
    await rest.create_message(channel=Constants.KICK_CLIPS_ANNOUNCEMENT_CHANNEL, content=messageContent)
    db.createWeeklyKickClipsData(f"{isoYear}:{isoWeek}",globals.kickClipMostViewsId, mostViewedUser, mostClipper)
    ResetClipGlobals()

def ResetClipGlobals():
    globals.kickClipMostViews = 0
    globals.kickClipMostViewsId = ''
    globals.kickClipMostViewedUser = {} 
    globals.kickClipMostClips = {}
    globals.kickClipMostViewsClipper = ''
    globals.kickClipMostViewsTitle = ''

def GetMostViewedClipper():
    mostViews = 0
    user = ''
    for clipperSlug, views in globals.kickClipMostViewedUser.items():
        if views > mostViews:
            mostViews = views
            user = clipperSlug
    return  user, mostViews

def GetMostClipper():
    mostClips = 0
    user = ''
    for clipperSlug, numClips in globals.kickClipMostClips.items():
        if len(numClips) > mostClips:
            mostClips = len(numClips)
            user = clipperSlug
    return user, mostClips