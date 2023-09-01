class Constants:
    DEBUG = False
    TEST_SERVER = False

    if TEST_SERVER:
        GUILD_ID =313876691082674178 #Guild ID of the discord server
        STDOUT_CHANNEL_ID =1137599805787480214 # Channel ID the bot will post notifications to
        whiteListedRoleIDs = [1096930045685145710] # IDs of Roles you wish to be white listed for some commands
    else:
        GUILD_ID =1058859922219081778 #Guild ID of the discord server
        STDOUT_CHANNEL_ID =1069865162573611058 # Channel ID the bot will post notifications to
        whiteListedRoleIDs = [1100148453792813086,1062179283705020486] # IDs of Roles you wish to be white listed for some commands

    WAIT_BETWEEN_MESSAGES = 1800 # minimum amount of time in seconds the stream has to be offline before new notification messages. 
    MIN_TIME_BEFORE_AVATAR_CHANGE = 48 # Minimum time before avatar changes -- in hours
    ONLINE_MESSAGE_REBROADCAST_TIME = 86400 #Time in seconds the stream will be online before another online notification will be broadcasted
    TIME_BEFORE_BOT_RESTART = 86400 #time in seconds before bot will restart
    TIME_OFFLINE_BEFORE_RESTART = 900 #minimum time in seconds stream needs to be offline before bot will restart IF TIME_BEFORE_BOT_RESTART time has been met

    ONLINE_CHECK_TIMER = 120 #Wait time in seconds between checks
    LONG_ONLINE_CHECK_TIMER = 600
    AVATAR_CHECK_TIMER = 130
    STATUS_CHECK_TIMER = 125
    RESTART_CHECK_TIMER = 300

    SMART_ALERT_LOOK_AHEAD = 3 #number of hours smart alert looks ahead to make sure conditions are still met (to make sure alerts are made too late into a stream)
    PERCENTAGE_OF_MAX = 0.85 # Percent of maximum users online before a smart alert goes off
    SECONDS_BETWEEN_SMART_ALERTS = 21600 # minimum number of seconds before another smart alert goes off

    RECORD_KEEPING_START_DATE = 1684210200 #Epoch time in seconds when you started using this bot Use: https://www.epochconverter.com/

    PIN_TIME_LONG = 4 # number in hours. If new image is found on twitter, image will be auto pinned for this length of time
    PIN_TIME_SHORT = 1 # same as above but this is used for images added via rebroadcast-image command

    streamerName = "LitneySpears"

    #Usernames associated with each platform - if not applicable leave an empty string. i.e. cbUserName = ''
    kickUserName = 'LitneySpears'
    cbUserName = ''
    fansUserName = 'Litneyspearsx'
    ofUserName = 'litneyspearsx'
    ytUserName = 'litneyspears_'
    twitchUserName = 'litneyspears_'
    cam4UserName = ''
    mfcUserName = ''
    bcUserName = ''
    scUserName = ''

    kickUrl = f'https://kick.com/{kickUserName}'
    fansUrl = f"https://fansly.com/{fansUserName}"
    ofUrl = f"https://onlyfans.com/{ofUserName}"
    ytUrl = f"https://www.youtube.com/@{ytUserName}/live"
    twitchUrl = f"https://www.twitch.tv/{twitchUserName}"
    cam4Url = f"https://www.cam4.com/{cam4UserName}"
    mfcUrl = f"https://www.myfreecams.com/#{mfcUserName}"
    bcUrl = f"https://bongacams.com/{bcUserName}"
    scUrl = f"https://stripchat.com/{scUserName}"

    
    #affiliate api link to see online users in cb https://chaturbate.com/affiliates/promotools/api_usersonline/
    # This makes assumptions thaty may not be true for your model, so go to the link above and make an API url for yourself. 
    # I've found this responds more reliably when you narrow down the search more. So add region, and any tags your model always uses
    cbApiUrl = "https://chaturbate.com/api/public/affiliates/onlinerooms/?wm=3pmuc&client_ip=request_ip&gender=f&region=northamerica&tag=bigboobs"

    # Links directly to the model's live stream - used for discord announcements.
    cbLiveStreamUrl = f"https://chaturbate.com/{cbUserName}/"
    OfLiveStreamUrl = f"https://onlyfans.com/{ofUserName}/live"
    fansLiveStreamUrl = f"https://fansly.com/live/{fansUserName}"
    twitchLiveStreamUrl = f"https://www.twitch.tv/{twitchUserName}"
    ytLiveStreamUrl = f"https://www.youtube.com/@{ytUserName}/live"
    kickLiveStreamUrl = f"https://kick.com/{kickUserName}"
    cam4LiveStreamUrl = f"https://www.cam4.com/{cam4UserName}"
    mfcLiveStreamUrl = f"https://www.myfreecams.com/#{mfcUserName}"
    bcLiveStreamUrl = f"https://bongacams.com/{bcUserName}"
    scLiveStreamUrl = f"https://stripchat.com/{scUserName}"

    cbOnlineText = streamerName + " is live on Chaturbate!\n<" + cbLiveStreamUrl + ">"
    ofOnlineText = streamerName + " is live on Onlyfans!\n<" + OfLiveStreamUrl + ">"
    fansOnlineText = streamerName + " is live on Fansly!\n<" + fansLiveStreamUrl + ">"
    twitchOnlineText = streamerName + " is live on Twitch!\n<" + twitchLiveStreamUrl + ">"
    ytOnlineText = streamerName + " is live on YouTube!\n<" + ytLiveStreamUrl + ">"
    kickOnlineText = streamerName + " is live on Kick!\n<" + kickLiveStreamUrl + ">"
    cam4OnlineText = streamerName + " is live on Cam4!\n<" + cam4LiveStreamUrl + ">"
    mfcOnlineText = streamerName + " is live on MyFreeCams!\n<" + mfcLiveStreamUrl + ">"
    bcOnlineText = streamerName + " is live on BongaCams!\n<" + bcLiveStreamUrl + ">"
    scOnlineText = streamerName + " is live on StripChat!\n<" + scLiveStreamUrl + ">"

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

    #Leave empty string if you don't use. twitterUrl = ""
    # pulls images from the twitter page, so if your streamer shares other stuff that isn't photos of her, probably don't use it. And just add the images yourself, or remove ones you don't want
    twitterUrl = 'https://twitter.com/Litney_Spears_' 
    
    linkTreeUrl = "https://allmylinks.com/litneyspears"

    fansDefaultTitle = "Naughty sleep stream? =)"
    ofDefaultTitle = "Naughty time? =)"
    cam4DefaultTitle = "Cam4 Naughty Time."
    mfcDefaultTitle = "MFC Fun Time."
    bcDefaultTitle = "BongaCams Fun Time."
    scDefaultTitle = "StripChat Fun Time."