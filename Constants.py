class Constants:
    DEBUG = False
    TEST_SERVER = False

    if TEST_SERVER:
        GUILD_ID =313876691082674178 #Guild ID of the discord server
        STDOUT_CHANNEL_ID =1096895456694505532 # Channel ID the bot will post notifications to
        whiteListedRoleIDs = [1096930045685145710]
    else:
        GUILD_ID =852965953309376582 #Guild ID of the discord server
        STDOUT_CHANNEL_ID =1074419703533015101 # Channel ID the bot will post notifications to
        whiteListedRoleIDs = [852971722424188940,852972290806906920,1045451879901057107]

    WAIT_BETWEEN_MESSAGES = 1800 # minimum amount of time in seconds the stream has to be offline before new notification messages. 
    MIN_TIME_BEFORE_AVATAR_CHANGE = 48 # Minimum time before avatar changes -- in hours
    ONLINE_MESSAGE_REBROADCAST_TIME = 86400 #Time in seconds the stream will be online before another online notification will be broadcasted
    TIME_BEFORE_BOT_RESTART = 604800 #time in seconds before bot will restart
    TIME_OFFLINE_BEFORE_RESTART = 900 #minimum time in seconds stream needs to be offline before bot will restart IF TIME_BEFORE_BOT_RESTART time has been met

    onlineCheckTimer = 120 #Wait time in seconds between checks
    longOnlineCheckTimer = 600
    avatarCheckTimer = 130
    statusCheckTimer = 125
    restartCheckTimer = 300

    recordKeepingStartDate = 1684210200 #Epoch time in seconds when you started using this bot Use: https://www.epochconverter.com/

    pinTimeLong = 16 # number in hours. If new image is found on twitter, image will be auto pinned for this length of time
    pinTimeShort = 1 # same as above but this is used for images added via rebroadcast-image command

    streamerName = "Cass"

    kickUserName = 'kittycass'
    kittiesKickUserName = 'casskitties'
    cbUserName = 'badkittycass'
    fansUserName = 'BadKittyCass'
    onlyUserName = 'badkittycass'
    ytUserName = 'kitty_cass_'
    casTwitchChannelName = 'kitty_goes_mreow'


    #Links to model pages - not necessarily the live streaming page - if not applicable leave an empty string ex. casKickUrl = ""
    casKickUrl = f'https://kick.com/{kickUserName}'
    kittiesKickUrl = f'https://kick.com/{kittiesKickUserName}'
    casFansUrl = f"https://fansly.com/{fansUserName}"
    casOnlyUrl = f"https://onlyfans.com/{onlyUserName}"
    casYtUrl = f"https://www.youtube.com/@{ytUserName}/live"

    #affiliate api link to see online users in cb https://chaturbate.com/affiliates/promotools/api_usersonline/
    # This makes assumptions thaty may not be true for your model, so go to the link above and make an API url for yourself. if not applicable leave an empty string ex. casKickUrl = ""
    # I've found this responds more reliably when you narrow down the search more. So add region, and any tags your model always uses
    casChatApiUrl = "https://chaturbate.com/api/public/affiliates/onlinerooms/?wm=3pmuc&client_ip=request_ip&gender=f&region=northamerica&tag=bigboobs" 

    # Links directly to the model's live stream - used for discord announcements. if not applicable leave an empty string ex. casKickUrl = ""
    cbLiveStreamUrl = f"https://chaturbate.com/{cbUserName}/"
    OfLiveStreamUrl = f"https://onlyfans.com/{onlyUserName}/live"
    fansLiveStreamUrl = f"https://fansly.com/live/{fansUserName}"
    twitchLiveStreamUrl = f"https://www.twitch.tv/{casTwitchChannelName}"
    ytLiveStreamUrl = f"https://www.youtube.com/@{ytUserName}/live"
    kickLiveStreamUrl = f"https://kick.com/{kickUserName}"

    chaturOnlineText = streamerName + " is live on Chaturbate!\n<" + cbLiveStreamUrl + ">"
    ofOnlineText = streamerName + " is live on Onlyfans!\n<" + OfLiveStreamUrl + ">"
    fansOnlineText = streamerName + " is live on Fansly!\n<" + fansLiveStreamUrl + ">"
    twitchOnlineText = streamerName + " is live on Twitch!\n" + twitchLiveStreamUrl
    ytOnlineText = streamerName + " is live on YouTube!\n" + ytLiveStreamUrl
    kickOnlineText = streamerName + " is live on Kick!\n<" + kickLiveStreamUrl + ">"
    kittiesKickOnlineText = "Cass' Kitties are live on Kick!\n<https://kick.com/casskitties>"

    kickEmbedColor = "#52fb19"
    fansEmbedColor = "#ffffff"
    ofEmbedColor = "#018ccf"
    cbEmbedColor = "#f6922f"

    #Leave empty string if you don't use. twitterUrl = ""
    # pulls images from the twitter page, so if your streamer shares other stuff that isn't photos of her, probably don't use it. And just add the images yourself, or remove ones you don't want
    twitterUrl = 'https://twitter.com/_kitty_cass_' 
    
    linkTreeUrl = "https://linktr.ee/kitty_cass_"

    fansDefaultTitle = "Naughty sleep stream? =)"
    ofDefaultTitle = "Naughty time? =)"