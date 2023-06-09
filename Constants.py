class Constants:
    DEBUG = True
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

    casKickUrl = 'https://kick.com/kittycass'
    kittiesKickUrl = 'https://kick.com/casskitties'
    casFansUrl = "https://fansly.com/BadKittyCass"
    casOnlyUrl = "https://onlyfans.com/badkittycass"
    casYtUrl = "https://www.youtube.com/@kitty_cass_/live"
    casChatApiUrl = "https://chaturbate.com/api/public/affiliates/onlinerooms/?wm=3pmuc&client_ip=request_ip&gender=f&region=northamerica&tag=bigboobs" #affiliate api link to see online users in cb
    cbUserName = 'badkittycass'
    casTwitchChannelName = 'kitty_goes_mreow' #twitch name, not url

    cbLiveStreamUrl = "https://chaturbate.com/badkittycass/"
    OfLiveStreamUrl = "https://onlyfans.com/badkittycass/live"
    fansLiveStreamUrl = "https://fansly.com/live/BadKittyCass"
    twitchLiveStreamUrl = "https://www.twitch.tv/kitty_goes_mreow"
    ytLiveStreamUrl = "https://www.youtube.com/@kitty_cass_/live"
    kickLiveStreamUrl = "https://kick.com/kittycass"

    streamerName = "Cass"

    chaturOnlineText = streamerName + " is live on Chaturbate!\n" + cbLiveStreamUrl
    ofOnlineText = streamerName + " is live on Onlyfans!\n" + OfLiveStreamUrl
    fansOnlineText = streamerName + " is live on Fansly!\n" + fansLiveStreamUrl
    twitchOnlineText = streamerName + " is live on Twitch!\n" + twitchLiveStreamUrl
    ytOnlineText = streamerName + " is live on YouTube!\n" + ytLiveStreamUrl
    kickOnlineText = streamerName + " is live on Kick!\n" + kickLiveStreamUrl
    kittiesKickOnlineText = "Cass' Kitties are live on Kick!\nhttps://kick.com/casskitties"

    kickEmbedColor = "#52fb19"
    fansEmbedColor = "#ffffff"
    ofEmbedColor = "#018ccf"

    twitterUrl = 'https://twitter.com/_kitty_cass_'
    linkTreeUrl = "https://linktr.ee/kitty_cass_"

    onlineCheckTimer = 120 #Wait time in seconds between checks
    avatarCheckTimer = 130
    statusCheckTimer = 125
    restartCheckTimer = 300

    recordKeepingStartDate = 1684210200 #Epoch time in seconds when you started using this bot Use: https://www.epochconverter.com/

    
