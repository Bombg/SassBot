class Constants:
    DEBUG = False
    TEST_SERVER = False
    if TEST_SERVER:
        GUILD_ID =313876691082674178 #Guild ID of the discord server
        whiteListedRoleIDs = [145802742647095296] # IDs of Roles you wish to be white listed for some commands. You can also add user IDs if you want to add an individual without a role
        # Channel ID the bot will post notifications to
        KICK_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        CB_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        FANS_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        OF_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        YT_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        TWITCH_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        CAM4_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        MFC_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        BC_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        SC_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        EP_NOTIFICATION_CHANNEL_ID = 1137599805787480214
        CONFESSTION_CHANNEL_ID = 1137599805787480214
        
        CONFESSION_COMMAND_ID = 1159423004346957835
        CONFESS_REVIEW_COMMAND_ID = 1159423004346957834
    else:
        GUILD_ID = 1174994456181755934 #Guild ID of the discord server
        whiteListedRoleIDs = [145802742647095296,1174591890608369664,1176074001362190346,1176080712865169429,1176080119534727178] # IDs of Roles you wish to be white listed for some commands. You can also add user IDs if you want to add an individual without a role
        # Channel ID the bot will post notifications to
        KICK_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        CB_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        FANS_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        OF_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        YT_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        TWITCH_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        CAM4_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        MFC_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        BC_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        SC_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        EP_NOTIFICATION_CHANNEL_ID = 1176083320157786143
        CONFESSTION_CHANNEL_ID = 1174994457561665598
        
        CONFESSION_COMMAND_ID = 1287575235910045699
        CONFESS_REVIEW_COMMAND_ID = 1287575235910045698

    WAIT_BETWEEN_MESSAGES = 1800 # minimum amount of time in seconds the stream has to be offline before new notification messages. 
    MIN_TIME_BEFORE_AVATAR_CHANGE = 48 # Minimum time before avatar changes -- in hours
    ONLINE_MESSAGE_REBROADCAST_TIME = 86400 #Time in seconds the stream will be online before another online notification will be broadcasted
    TIME_BEFORE_BOT_RESTART = 86400 #time in seconds before bot will restart
    TIME_OFFLINE_BEFORE_RESTART = 900 #minimum time in seconds stream needs to be offline before bot will restart IF TIME_BEFORE_BOT_RESTART time has been met
    TEMP_TITLE_UPTIME = 57600 #Time in seconds temp titles will be used before default titles are used
    TIME_BEFORE_REVIEW_RESET = 300 # Time a whitelisted person has to review a confession before its added back to the queue
    
    # Nodriver default for retries is 4, but for slow machines this could require a lot more (raspberry pi 3b+ tested with 20 and still fails occasionally)
    NODRIVER_BROWSER_CONNECT_RETRIES = 25

    # Platform Check Timers - all in seconds
    KICK_CHECK_TIMER = 180
    CB_CHECK_TIMER = 180
    FANS_CHECK_TIMER = 220
    OF_CHECK_TIMER = 170
    YT_CHECK_TIMER = 180
    TWITCH_CHECK_TIMER = 180
    CAM4_CHECK_TIMER = 1800 # Using very long Cam4 check timer to be on safe side. Lower at your own risk. Still unsure if safe.
    MFC_CHECK_TIMER = 180
    BC_CHECK_TIMER = 180
    SC_CHECK_TIMER = 180
    EP_CHECK_TIMER = 180

    AVATAR_CHECK_TIMER = 130 # Timer for checking last online time before changing between happy/angry avatars
    STATUS_CHECK_TIMER = 125 # Timer for checking online status and changing the bot status. Also used for record keeping
    CONFESSION_CHECK_TIMER = 20 # How often new confessions are checked 

    CONFESSION_ALERT_INTERVALS = [0,0,1800,7200,18000,43200] # Seconds between unreveiwed confession alerts. Starts at index 1. 1st alert 0 seconds, 2nd alert 1800 etc. New confessions reset count

    SMART_ALERT_LOOK_AHEAD = 3 #number of hours smart alert looks ahead to make sure conditions are still met (to make sure alerts aren't made too late into a stream)
    PERCENTAGE_OF_MAX = 0.85 # Percent of maximum users online before a smart alert goes off
    SECONDS_BETWEEN_SMART_ALERTS = 21600 # minimum number of seconds before another smart alert goes off

    RECORD_KEEPING_START_DATE = 1727022585 #Epoch time in seconds when you started using this bot Use: https://www.epochconverter.com/

    PIN_TIME_LONG = 4 # number in hours. 
    PIN_TIME_SHORT = 1 # same as above but this is used for images added via rebroadcast-image command

    # For role pings to work you will first need to turn them on via the /ping-toggle True/False command. 
    # if you don't want a specific platform to get a ping, just leave an empty string
    # If you wish to ping everyone simply input @everyone, but if you wish to ping a specific role you'll need to get the role ID and assemble it like so <@&putRoleIDHere>
    # for example if the role id is 999 then you'd put ROLES_TO_PING = '<@&999> '
    # If you want to ping multiple roles then just put them in the same string. i.e. ROLES_TO_PING = '<@&999> @everyone '
    # Leave a space at the end of the string i.e ROLES_TO_PING = '@everyone '
    KICK_ROLES_TO_PING = "@everyone "
    CB_ROLES_TO_PING = "@everyone "
    FANS_ROLES_TO_PING = "@everyone "
    OF_ROLES_TO_PING = "@everyone "
    YT_ROLES_TO_PING = "@everyone "
    TWITCH_ROLES_TO_PING = "@everyone "
    CAM4_ROLES_TO_PING = "@everyone "
    MFC_ROLES_TO_PING = "@everyone "
    BC_ROLES_TO_PING = "@everyone "
    SC_ROLES_TO_PING = "@everyone "
    EP_ROLES_TO_PING = "@everyone "

    # For rerun announcements/pings to work you will first need to turn them on via the /announce-rerun-toggle True/False command AND the /ping-toggle True/False command. 
    # if you don't want a specific platform to get a rerun ping, just leave an empty string (It will still get announced if turned on)
    # If you wish to ping everyone simply input @everyone, but if you wish to ping a specific role you'll need to get the role ID and assemble it like so <@&putRoleIDHere>
    # for example if the role id is 999 then you'd put ROLES_TO_PING = '<@&999> '
    # If you want to ping multiple roles then just put them in the same string. i.e. ROLES_TO_PING = '<@&999> @everyone '
    # Leave a space at the end of the string i.e ROLES_TO_PING = '@everyone '
    KICK_RERUN_ROLES_TO_PING = ""
    CB_RERUN_ROLES_TO_PING = ""
    FANS_RERUN_ROLES_TO_PING = ""
    OF_RERUN_ROLES_TO_PING = ""
    YT_RERUN_ROLES_TO_PING = ""
    TWITCH_RERUN_ROLES_TO_PING = ""
    CAM4_RERUN_ROLES_TO_PING = ""
    MFC_RERUN_ROLES_TO_PING = ""
    BC_RERUN_ROLES_TO_PING = ""
    SC_RERUN_ROLES_TO_PING = ""
    EP_RERUN_ROLES_TO_PING = ""

    #Generic name of the streamer that will be used for all notifications
    streamerName = "FlexieFae"

    #Usernames associated with each platform - if not applicable leave an empty array. i.e. cbUserName = []
    #If the streamer has multiple accounts for a paltform, add an extra username to the array i.e. cbUserName = ['user1','user2']
    kickUserName = ['flexiefae']
    cbUserName = ['heynicole01']
    fansUserName = ['FlexieFae']
    ofUserName = []
    ytUserName = ['FlexieFae']
    twitchUserName = ['flexiefae']
    cam4UserName = []
    mfcUserName = []
    bcUserName = []
    scUserName = []
    epUserName = []

    twitchUrl = f"https://www.twitch.tv/flexiefae" #Add a valid twitch URL here even if you streamer doesn't have twitch or else the presence won't update properly

    #affiliate api link to see online users in cb https://chaturbate.com/affiliates/promotools/api_usersonline/
    # This makes assumptions thaty may not be true for your model, so go to the link above and make an API url for yourself. 
    # I've found this responds more reliably when you narrow down the search more. So add region, and any tags your model always uses
    cbJsonLimit = 500 # 500 is max. 100 is default if you remove the limit tag. Keep the limit tag in the api url OR change this to 100 if the tag is removed
    cbApiUrl = f"https://chaturbate.com/api/public/affiliates/onlinerooms/?wm=3pmuc&client_ip=request_ip&gender=f&region=northamerica&limit={cbJsonLimit}"
    
    # Colors the line that runs vertically on the left side of the embed. Also used to color graphs
    kickEmbedColor = "#52fb19"
    fansEmbedColor = "#a0816c"
    ofEmbedColor = "#018ccf"
    cbEmbedColor = "#f6922f"
    ytEmbedColor = "#ff0000"
    twitchEmbedColor = "#9146FF"
    cam4EmbedColor = "#dd5d2c"
    mfcEmbedColor = "#377c1d"
    bcEmbedColor = "#97323a"
    scEmbedColor = "#a02831"
    epEmbedColor = "#f03d4c"

    # Mainly Used in stream-status command
    linkTreeUrl = "https://allmylinks.com/flexiefae"
    
    # Titles for announcement embeds
    # Titles for platforms that have optional titles or no titles at all
    # You can also use the /title command to create temporary titles for a platform on the fly, but once the TEMP_TITLE_UPTIME time is up then it defaults back to these titles
    # If the titles contain any variation of RR/Rerun/not live then it will be detected by rerun detection
    fansDefaultTitle = "Naughty Fansly stream? =)"
    ofDefaultTitle = "Naughty time? =)"
    cam4DefaultTitle = "Cam4 Naughty Time."
    mfcDefaultTitle = "MFC Fun Time."
    bcDefaultTitle = "BongaCams Fun Time."
    scDefaultTitle = "StripChat Fun Time."
    epDefaultTitle = "ePlay Fun Time."
    
    # This is the text that will appear above the embed. Role mentions will be added before this text, and a link to the stream will be added after
    # i.e. @everyone <AboveEmbedTextGoesHere> https://kick.com/StreamerName
    kickAboveEmbedText =  f"{streamerName} is live on Kick!"
    fansAboveEmbedText =  f"{streamerName} is live on Fansly!"
    ofAboveEmbedText =  f"{streamerName} is live on Onlyfans!"
    cbAboveEmbedText =  f"{streamerName} is live on Chaturbate!"
    ytAboveEmbedText =  f"{streamerName} is live on YouTube!"
    twitchAboveEmbedText =  f"{streamerName} is live on Twitch!"
    cam4AboveEmbedText =  f"{streamerName} is live on Cam4!"
    mfcAboveEmbedText =  f"{streamerName} is live on MyFreeCams!"
    bcAboveEmbedText =  f"{streamerName} is live on BongaCams!"
    scAboveEmbedText =  f"{streamerName} is live on StripChat!"
    epAboveEmbedText =  f"{streamerName} is live on ePlay!"

    # This is small text that will appear below the title, and above the main image inside the embed.
    kickBelowTitleText =  f"{streamerName} is now live on Kick!"
    fansBelowTitleText =  f"{streamerName} is now live on Fansly!"
    ofBelowTitleText =  f"{streamerName} is now live on Onlyfans!"
    cbBelowTitleText =  f"{streamerName} is now live on Chaturbate!"
    ytBelowTitleText =  f"{streamerName} is now live on YouTube!"
    twitchBelowTitleText =  f"{streamerName} is now live on Twitch!"
    cam4BelowTitleText =  f"{streamerName} is now live on Cam4!"
    mfcBelowTitleText =  f"{streamerName} is now live on MyFreeCams!"
    bcBelowTitleText =  f"{streamerName} is now live on BongaCams!"
    scBelowTitleText =  f"{streamerName} is now live on StripChat!"
    epBelowTitleText =  f"{streamerName} is now live on ePlay!"