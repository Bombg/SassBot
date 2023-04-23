class Constants:
    GUILD_ID =852965953309376582 #Guild ID of the discord server
    STDOUT_CHANNEL_ID =1074419703533015101 # Channel ID the bot will post notifications to
    WAIT_BETWEEN_MESSAGES = 30 # minimum amount of time the stream has to be offline before new notification messages. 1 = one interval of onlineCheckTimer
    MIN_TIME_BEFORE_AVATAR_CHANGE = 48 # Minimum time before avatar changes -- in hours
    ONLINE_MESSAGE_REBROADCAST_TIME = 86400 #Time in seconds the stream will be online before another online notification will be broadcasted
    TIME_BEFORE_BOT_RESTART = 86400 #time in seconds before bot will restart
    TIME_OFFLINE_BEFORE_RESTART = 900 #minimum time in seconds stream needs to be offline before bot will restart IF TIME_BEFORE_BOT_RESTART time has been met

    casKickUrl = 'https://kick.com/kittycass'
    kittiesKickUrl = 'https://kick.com/casskitties'
    casFansUrl = "https://fansly.com/BadKittyCass"
    casOnlyUrl = "https://onlyfans.com/badkittycass"
    casYtUrl = "https://www.youtube.com/@kitty_cass_/live"
    casChatApiUrl = "https://chaturbate.com/api/public/affiliates/onlinerooms/?wm=3pmuc&client_ip=request_ip&gender=f&region=northamerica&tag=bigboobs" #affiliate api link to see online users in cb
    casTwitchChannelName = 'kitty_goes_mreow' #twitch name, not url

    chaturOnlineText = "Cass is live on Chaturbate!\nhttps://chaturbate.com/badkittycass/"
    ofOnlineText = "Cass is live on Onlyfans!\nhttps://onlyfans.com/badkittycass/live"
    fansOnlineText = "Cass is live on Fansly!\nhttps://fansly.com/live/BadKittyCass"
    twitchOnlineText = "Cass is live on Twitch!\nhttps://www.twitch.tv/kitty_goes_mreow"
    ytOnlineText = "Cass is live on YouTube!\nhttps://www.youtube.com/@kitty_cass_/live"
    kickOnlineText = "Cass is live on Kick!\nhttps://kick.com/kittycass"
    kittiesKickOnlineText = "Cass' Kitties are live on Kick!\nhttps://kick.com/casskitties"

    onlineCheckTimer = 120 #Wait time in seconds between checks
    avatarCheckTimer = 130
    statusCheckTimer = 125
    restartCheckTimer = 300

    whiteListedIds = [145802742647095296,427890651510603778,966474683379744849,485741419303010325,278312496131997700,338783926933913602,1069673585884541058,306368812054216704]
