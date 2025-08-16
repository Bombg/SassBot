from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from typing import Optional

#from typing import ClassVar # ClassVar[int] - not changeable by .env and no instantiation required
#from pydantic import computed_field
#   @computed_field
#     @property
#     def onlineString(self) -> str:
#         return f"{self.streamerName} is online"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    SASSBOT_LOG_LEVEL:int = 20 # DEBUG = 10, INFO = 20, WARNING = 30, ERROR = 40, CRITICAL = 50
    OTHER_LIBRARIES_LOG_LEVEL:int = 20 # DEBUG = 10, INFO = 20, WARNING = 30, ERROR = 40, CRITICAL = 50

    SECRET:str = ''
    GUILD_ID:int = 0 #Guild ID of the discord server
    whiteListedRoleIDs:list[int] = [] # IDs of Roles you wish to be white listed for some commands. You can also add user IDs if you want to add an individual without a role
    MOD_ROLE_ID:int = 0 # Used to ping mods to take action on an approved ban appeal
    # Channel ID the bot will post notifications to
    KICK_NOTIFICATION_CHANNEL_ID:int = 0
    CB_NOTIFICATION_CHANNEL_ID:int = 0
    FANS_NOTIFICATION_CHANNEL_ID:int = 0
    OF_NOTIFICATION_CHANNEL_ID:int = 0
    YT_NOTIFICATION_CHANNEL_ID:int = 0
    TWITCH_NOTIFICATION_CHANNEL_ID:int = 0
    CAM4_NOTIFICATION_CHANNEL_ID:int = 0
    MFC_NOTIFICATION_CHANNEL_ID:int = 0
    BC_NOTIFICATION_CHANNEL_ID:int = 0
    SC_NOTIFICATION_CHANNEL_ID:int = 0
    EP_NOTIFICATION_CHANNEL_ID:int = 0
    MV_NOTIFICATION_CHANNEL_ID:int = 0
    CONFESSTION_CHANNEL_ID:int = 0
    APPEAL_CHANNEL_ID:int = 0
    KICK_CLIPS_ANNOUNCEMENT_CHANNEL:int = 0
    
    CONFESSION_COMMAND_ID:int = 0
    CONFESS_REVIEW_COMMAND_ID:int = 0
    APPEAL_COMMAND_ID:int = 0
    APPEAL_REVIEW_COMMAND_ID:int = 0
    
    # Leave an empty string if you don't wish to use a proxy for a checker.
    # Kick/OF/Fansly use nodriver, which doesn't support authenticated proxies
    # All the other platforms assumes you're using a socks5 proxy, so you can leave out the socks5:// part
    # Commented out platforms don't support proxies 
    KICK_PROXY:str = "" # Chrome/Chromium doesn't support authenticated proxies
    FANS_PROXY:str = "" # Chrome/Chromium doesn't support authenticated proxies
    OF_PROXY:str = ""# Chrome/Chromium doesn't support authenticated proxies
    #CB_PROXY = "" # Everything below assumed is a socks5 proxy.
    MV_PROXY:str = ""
    BC_PROXY:str = ""
    SC_PROXY:str = ""
    EP_PROXY:str = ""
    CAM4_PROXY:str = ""
    MFC_PROXY:str = ""
    #YT_PROXY = ""
    #TWITCH_PROXY = ""

    WAIT_BETWEEN_MESSAGES:int = 1800 # minimum amount of time in seconds the stream has to be offline before new notification messages. 
    MIN_TIME_BEFORE_AVATAR_CHANGE:int = 48 # Minimum time before avatar changes -- in hours
    ONLINE_MESSAGE_REBROADCAST_TIME:int = 86400 #Time in seconds the stream will be online before another online notification will be broadcasted
    TIME_BEFORE_BOT_RESTART:int = 86400 #time in seconds before bot will restart. Restart checks are made every 10 minutes
    TIME_OFFLINE_BEFORE_RESTART:int = 900 #minimum time in seconds stream needs to be offline before bot will restart IF TIME_BEFORE_BOT_RESTART time has been met
    TEMP_TITLE_UPTIME:int = 57600 #Time in seconds temp titles will be used before default titles are used
    TIME_BEFORE_REVIEW_RESET:int = 300 # Time a whitelisted person has to review a confession before its added back to the queue
    
    # Nodriver default for retries is 4, but for slow machines this could require a lot more (raspberry pi 3b+ tested with 20 and still fails occasionally)
    NODRIVER_BROWSER_CONNECT_RETRIES:int = 25
    NODRIVER_WAIT_MULTIPLIER:int = 8 # multiplier for nodriver waits. Make this longer for slower machines

    # Platform Check Timers - all in seconds
    KICK_CHECK_TIMER:int = 180
    CB_CHECK_TIMER:int = 180
    FANS_CHECK_TIMER:int = 220
    OF_CHECK_TIMER:int = 170
    YT_CHECK_TIMER:int = 180
    TWITCH_CHECK_TIMER:int = 180
    CAM4_CHECK_TIMER:int = 1800 # Using very long Cam4 check timer to be on safe side. Lower at your own risk. Still unsure if safe.
    MFC_CHECK_TIMER:int = 180
    BC_CHECK_TIMER:int = 180
    SC_CHECK_TIMER:int = 180
    EP_CHECK_TIMER:int = 180
    MV_CHECK_TIMER:int = 180

    AVATAR_CHECK_TIMER:int = 130 # Timer for checking last online time before changing between happy/angry avatars
    STATUS_CHECK_TIMER:int = 125 # Timer for checking online status and changing the bot status. Also used for record keeping
    CONFESSION_CHECK_TIMER:int = 20 # How often new confessions are checked 
    APPEAL_CHECK_TIMER:int = 20 # How often new appeals are checked
    ROLE_ADD_REMOVE_TIMER:int = 15 # Time in between checks to add and remove roles

    CONFESSION_ALERT_INTERVALS:list[int] = [0,0,1800,7200,18000,43200] # Seconds between unreveiwed confession alerts. Starts at index 1. 1st alert 0 seconds, 2nd alert 1800 etc. New confessions reset count
    APPEAL_ALERT_INTERVALS:list[int] = [0,0,1800,7200,18000,43200] # Seconds between unreveiwed appeal alerts. Starts at index 1. 1st alert 0 seconds, 2nd alert 1800 etc. New appeals reset count

    SMART_ALERT_LOOK_AHEAD:int = 3 #number of hours smart alert looks ahead to make sure conditions are still met (to make sure alerts aren't made too late into a stream)
    PERCENTAGE_OF_MAX:float = 0.85 # Percent of maximum users online before a smart alert goes off
    SECONDS_BETWEEN_SMART_ALERTS:int = 21600 # minimum number of seconds before another smart alert goes off

    RECORD_KEEPING_START_DATE:int = 0 #Epoch time in seconds when you started using this bot Use: https://www.epochconverter.com/

    PIN_TIME_LONG:int = 4 # number in hours. 
    PIN_TIME_SHORT:int = 1 # same as above but this is used for images added via rebroadcast-image command

    # For role pings to work you will first need to turn them on via the /ping-toggle True/False command. 
    # if you don't want a specific platform to get a ping, just leave an empty string
    # If you wish to ping everyone simply input @everyone, but if you wish to ping a specific role you'll need to get the role ID and assemble it like so <@&putRoleIDHere>
    # for example if the role id is 999 then you'd put ROLES_TO_PING = '<@&999> '
    # If you want to ping multiple roles then just put them in the same string. i.e. ROLES_TO_PING = '<@&999> @everyone '
    # Leave a space at the end of the string i.e ROLES_TO_PING = '@everyone '
    KICK_ROLES_TO_PING:str = "@everyone "
    CB_ROLES_TO_PING:str = "@everyone "
    FANS_ROLES_TO_PING:str = "@everyone "
    OF_ROLES_TO_PING:str = "@everyone "
    YT_ROLES_TO_PING:str = "@everyone "
    TWITCH_ROLES_TO_PING:str = "@everyone "
    CAM4_ROLES_TO_PING:str = "@everyone "
    MFC_ROLES_TO_PING:str = "@everyone "
    BC_ROLES_TO_PING:str = "@everyone "
    SC_ROLES_TO_PING:str = "@everyone "
    EP_ROLES_TO_PING:str = "@everyone "
    MV_ROLES_TO_PING:str = "@everyone "

    # For rerun announcements/pings to work you will first need to turn them on via the /announce-rerun-toggle True/False command AND the /ping-toggle True/False command. 
    # if you don't want a specific platform to get a rerun ping, just leave an empty string (It will still get announced if turned on)
    # If you wish to ping everyone simply input @everyone, but if you wish to ping a specific role you'll need to get the role ID and assemble it like so <@&putRoleIDHere>
    # for example if the role id is 999 then you'd put ROLES_TO_PING = '<@&999> '
    # If you want to ping multiple roles then just put them in the same string. i.e. ROLES_TO_PING = '<@&999> @everyone '
    # Leave a space at the end of the string i.e ROLES_TO_PING = '@everyone '
    KICK_RERUN_ROLES_TO_PING:str = ""
    CB_RERUN_ROLES_TO_PING:str = ""
    FANS_RERUN_ROLES_TO_PING:str = ""
    OF_RERUN_ROLES_TO_PING:str = ""
    YT_RERUN_ROLES_TO_PING:str = ""
    TWITCH_RERUN_ROLES_TO_PING:str = ""
    CAM4_RERUN_ROLES_TO_PING:str = ""
    MFC_RERUN_ROLES_TO_PING:str = ""
    BC_RERUN_ROLES_TO_PING:str = ""
    SC_RERUN_ROLES_TO_PING:str = ""
    EP_RERUN_ROLES_TO_PING:str = ""
    MV_RERUN_ROLES_TO_PING:str = ""

    #Generic name of the streamer that will be used for all notifications
    streamerName:str = "Streamer"

    #Usernames associated with each platform - if not applicable leave an empty array. i.e. cbUserName = []
    #If the streamer has multiple accounts for a paltform, add an extra username to the array i.e. cbUserName = ['user1','user2']
    kickUserName:list[str] = []
    cbUserName:list[str] = []
    fansUserName:list[str] = []
    ofUserName:list[str] = []
    ytUserName:list[str] = []
    twitchUserName:list[str] = []
    cam4UserName:list[str] = []
    mfcUserName:list[str] = []
    bcUserName:list[str] = []
    scUserName:list[str] = []
    epUserName:list[str] = []
    mvUserName:list[str] = [] #case sensitive if you want the the avatar to be pulled

    twitchUrl:str = "https://www.example.com" #Add a valid url here or else the presence won't update properly

    banAppealButtonMessage:str = "# To appeal a ban, click the button below and fill out the form"
    confessButtonMessage:str = "# Submit your anonymous confessions"

    # Required if you want to use /health endpoint 
    # Required for Kick API use
    webhookPort:int = 6061 # what port to use to listen to webhooks or health checks (int not str). If left as a blank string then webhook/health check client (fastapi) wont be started
    webhookHostIp:str = '0.0.0.0' # 127.0.0.1 if you want to host locally. 0.0.0.0 if you want to be accessable from outside IPs. Check fastAPI docs for more info
    badHealthMultiplier:int = 2 # if badHealthMultiplier * shortest of the check timers is < last check time /health returns 503

    healthEndpoint:str = "/health"
    webhookEndpoint:str = "/webhook"
    kickOathCallbackEndpoint:str = "/callback"

    #Optional - but faster and more reliable if you setup an app on kick-- start one on the developer tab in kick settings
    kickClientId:str = ""
    kickClientSecret:str = ""
    kickChatroomId:str = '' # https://kick.com/api/v2/channels/<KICKUSERNAME> go here to get the ID's needed
    kickChannelId:str = ''
    kickRedirectUrl:str = '' #Must match EXACTLY with the redirect URL entered into kick dev dashboard
    kickDiscordRedirect:str = '' # Discord link to the server the user has connected their kick account to. Or whatever you want to redirect to after successful Oauth flow
    hasRolePermissions:bool = False # if the bot has permissions to change roles for kick sub roles
    kickLongRoleId:int = 0 #IDs for the roles you give to people who sub. Long is for month long subs
    kickShortRoleId:int = 0 # Short is meant for one day discord shows
    kickSubsShortThreshold:int = 5 # Number of subs to get the Short Role
    kickSubsShortLookBackHours:int = 12 # Hours, how far back to look into sub history to go towards threshold
    kickSubsLongThreshold:int = 1 # Number of subs to get the Long Role
    kickSubsLongLookBackDays:int = 31 # Days, how far back to look into sub history to go towards threshold
    kickLongDateRolePeriod:int = 31 # Days, how long user keeps the role before its removed
    kickShortTimeRolePeriod:int = 14 # Hours, how long user keeps role before it's removed
    kickConnectButtonMessage:str = "# Connect your Kick and Discord Accounts! \n ### This will allow you to gain special Discord roles when you sub on Kick"
    kickClipDaysLookBack:int = 30 # Number of days to look back for the weekly clip announcement

    #affiliate api link to see online users in cb https://chaturbate.com/affiliates/promotools/api_usersonline/
    # This makes assumptions thaty may not be true for your model, so go to the link above and make an API url for yourself. 
    # I've found this responds more reliably when you narrow down the search more. So add region, and any tags your model always uses
    cbJsonLimit:int = 500 # 500 is max. 100 is default. Limit tag will be added so that's not needed
    cbApiUrl:str = "https://chaturbate.com/api/public/affiliates/onlinerooms/?wm=3pmuc&client_ip=request_ip&gender=f&region=northamerica"
    
    # Colors the line that runs vertically on the left side of the embed. Also used to color graphs
    kickEmbedColor:str = "#52fb19"
    fansEmbedColor:str = "#a0816c"
    ofEmbedColor:str = "#018ccf"
    cbEmbedColor:str = "#f6922f"
    ytEmbedColor:str = "#ff0000"
    twitchEmbedColor:str = "#9146FF"
    cam4EmbedColor:str = "#dd5d2c"
    mfcEmbedColor:str = "#377c1d"
    bcEmbedColor:str = "#97323a"
    scEmbedColor:str = "#a02831"
    epEmbedColor:str = "#f03d4c"
    mvEmbedColor:str = "#722a9e"

    # Mainly Used in stream-status command
    linkTreeUrl:str = "https://allmylinks.com"
    
    # Titles for announcement embeds
    # Titles for platforms that have optional titles or no titles at all
    # You can also use the /title command to create temporary titles for a platform on the fly, but once the TEMP_TITLE_UPTIME time is up then it defaults back to these titles
    # If the titles contain any variation of RR/Rerun/not live then it will be detected by rerun detection
    fansDefaultTitle:str = "🍑💦Now taking good vibes on stream! =)🍑💦"
    ofDefaultTitle:str = "Naughty time? =)"
    cam4DefaultTitle:str = "Cam4 Naughty Time."
    mfcDefaultTitle:str = "MFC Fun Time."
    bcDefaultTitle:str = "BongaCams Fun Time."
    scDefaultTitle:str = "StripChat Fun Time."
    epDefaultTitle:str = "ePlay Fun Time."
    mvDefaultTitle:str = "Manyvids Fun Time Starts Now!"
    
    # This is the text that will appear above the embed. Role mentions will be added before this text, and a link to the stream will be added after
    # i.e. @everyone <AboveEmbedTextGoesHere> https://kick.com/StreamerName
    kickAboveEmbedText:Optional[str] = None
    fansAboveEmbedText:Optional[str] = None
    ofAboveEmbedText:Optional[str] = None
    cbAboveEmbedText:Optional[str] = None
    ytAboveEmbedText:Optional[str] = None
    twitchAboveEmbedText:Optional[str] = None
    cam4AboveEmbedText:Optional[str] = None
    mfcAboveEmbedText:Optional[str] = None
    bcAboveEmbedText:Optional[str] = None
    scAboveEmbedText:Optional[str] = None
    epAboveEmbedText:Optional[str] = None
    mvAboveEmbedText:Optional[str] = None

    @model_validator(mode="after")
    def CreateAboveEmbedText(self):
        self.kickAboveEmbedText = f"{self.streamerName} is live on Kick!"
        self.fansAboveEmbedText= f"{self.streamerName} is live on Fansly!"
        self.ofAboveEmbedText = f"{self.streamerName} is live on Onlyfans!"
        self.cbAboveEmbedText = f"{self.streamerName} is live on Chaturbate!"
        self.ytAboveEmbedText = f"{self.streamerName} is live on YouTube!"
        self.twitchAboveEmbedText = f"{self.streamerName} is live on Twitch!"
        self.cam4AboveEmbedText = f"{self.streamerName} is live on Cam4!"
        self.mfcAboveEmbedText = f"{self.streamerName} is live on MyFreeCams!"
        self.bcAboveEmbedText = f"{self.streamerName} is live on BongaCams!"
        self.scAboveEmbedText = f"{self.streamerName} is live on StripChat!"
        self.epAboveEmbedText = f"{self.streamerName} is live on ePlay!"
        self.mvAboveEmbedText = f"{self.streamerName} is live on ManyVids!"
        return self

    # This is small text that will appear below the title, and above the main image inside the embed.
    kickBelowTitleText:Optional[str] =None
    fansBelowTitleText:Optional[str] = None
    ofBelowTitleText:Optional[str] = None
    cbBelowTitleText:Optional[str] = None
    ytBelowTitleText:Optional[str] = None
    twitchBelowTitleText:Optional[str] = None
    cam4BelowTitleText:Optional[str] =None
    mfcBelowTitleText:Optional[str] = None
    bcBelowTitleText:Optional[str] = None
    scBelowTitleText:Optional[str] = None
    epBelowTitleText:Optional[str] = None
    mvBelowTitleText:Optional[str] = None

    @model_validator(mode="after")
    def CreateBelowTitleText(self):
        self.kickBelowTitleText = f"{self.streamerName} is now live on Kick!"
        self.fansBelowTitleText = f"{self.streamerName} is now live on Fansly!"
        self.ofBelowTitleText = f"{self.streamerName} is now live on Onlyfans!"
        self.cbBelowTitleText = f"{self.streamerName} is now live on Chaturbate!"
        self.ytBelowTitleText = f"{self.streamerName} is now live on YouTube!"
        self.twitchBelowTitleText = f"{self.streamerName} is now live on Twitch!"
        self.cam4BelowTitleText = f"{self.streamerName} is now live on Cam4!"
        self.mfcBelowTitleText = f"{self.streamerName} is now live on MyFreeCams!"
        self.bcBelowTitleText = f"{self.streamerName} is now live on BongaCams!"
        self.scBelowTitleText = f"{self.streamerName} is now live on StripChat!"
        self.epBelowTitleText = f"{self.streamerName} is now live on ePlay!"
        self.mvBelowTitleText = f"{self.streamerName} is now live on ManyVids!"
        return self

    # Leave empty strings if you want to use default thumbnail behavior; which is: (1)pull thumbnail from platform, (2)if it doesn't exist use image from image list, (3)if list empty use defaultThumbnail
    # Add your own image path/url if you want to exclusively use the same image over and over for a specific platform's thumbnail
    # If you want thumbnails to only come from the image list, make the string equal to LIST i.e cbThumbnail = "LIST" . Useful if you don't want NSFW thumbnails in alerts
    kickThumbnail:str = ""
    fansThumbnail:str = ""
    ofThumbnail:str = ""
    cbThumbnail:str = ""
    ytThumbnail:str = ""
    twitchThumbnail:str = ""
    cam4Thumbnail:str = ""
    mfcThumbnail:str = ""
    bcThumbnail:str = ""
    scThumbnail:str = ""
    epThumbnail:str = ""
    mvThumbnail:str = ""

    # Icon in this case is the small image that shows in the top left of the imbed before the streamer's name for that platform
    # This is used if an avatar/icon can't be found on a platform, otherwise the platform's version will be used
    defaultIcon:str = 'images/errIcon.png'

    # This thumbnail is used if there is no thumbnail for a platform AND there is nothing in the image list
    defaultThumbnail:str = 'images/twitErrImg.jpg'

    # Calm is default bot avatar, pissed is what it changes to after MIN_TIME_BEFORE_AVATAR_CHANGE has been met
    # Make them the same image if you don't want the feature to change anything 
    calmAvatar:str = 'images/avatars/calmStreamer.png'
    pissedAvatar:str = 'images/avatars/pissedStreamer.png'