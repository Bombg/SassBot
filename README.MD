# SassBot
## Discord bot for your favorite e-girl
### Platforms Supported:
- Twitch
- Kick
- Youtube
- Onlyfans
- Fansly
- Chaturbate
- Cam4
- MyFreeCams
- BongaCams
- StripChat
- ePlay
### Features
- Get notifications when your streamer is online sent to a discord channel
- Rerun detection/support. If stream titles contains a variation of rerun/rr/not live then it will be detected as a rerun.
    - by default reruns won't be announced, but you can choose to announce them to custom roles just for reruns
- Track multiple accounts per platform. (for example, if they have a paid and free account)
- There's a minimum time between notifications, so your discord members won't get spammed if you're having connection issues.
- Bot's status reflects what the streamer is doing. Offline or streaming on Kick, yt, etc.
- Auto embed images from Twitter into notifications
    - feature is busted for now until Twitter allows people to see tweets without being logged in once again.
- White list commands to certain roles.
- Log who uses what commands
- Add/remove images yourself to embed into notifications via image commands. Images are rotated through, so add as many as you like.
- Rebroadcast online notifications with rebroadcast commands
- Subathon online timers via subathon commands
- Send alerts during peak discord usage times
- ... and many more!
### Commands
- /stream-status - See if your streamer is currently offline or online. Shows time online/offline and total time streamed.
- /ping-toggle - Toggle for role pings in online announcements. This is defaulted to false, so set true if you want role pings
- /announce-rerun-toggle - Toggle if reruns will be announced. If a title contains a variation of rr/rerun/not live then the stream will be detected as a rerun.
- /title  - Allows you to temporarily add a custom title for a platform/username combo. TEMP_TITLE_UPTIME in constants.py determines how long a temp title added via /title will be used for.
- Image list commands - Images can be pulled from twitter and/or manually added. These images are used for embeds for all supported platforms.
    - /image-list-show - show the list of image urls that will be rotated through during online announcements
    - /image-list-add -  add an image url to the image list
    - /image-list-remove -  remove an image from the image list. Must provide the url
- Pin image commands -  If there is no pinned image, Kick, Twitch, CB, and YT use thumbnail images from the video feed, OF/Fans will embed images from the image list. 
    - /image-pin - pin an image for a number of hours you choose. Pinned images will be embedded into notifications in the announcements channel.
    - /image-check-pin  - Check to see if an image is pinned
    - /image-unpin  - unpin an image if it is pinned.
- /rebroadcast - Send out online notifications to the announcements channel IF the streamer is online. Isn't isntant but goes off when the next online check is made.
    - /rebroadcast-image  - same as above but you can attach a URL of an image to embed into the new announcement(s)
- Subathon Commands - apart from commands, subathon status is also displayed in the Bot's status.
    - /subathon - check the status of the current subathon, if there is one.
    - /subathon-start - start a subathon timer
    - /subathon-end - end a subathon timer
- Stats
    - /users-graph Get a graph of online/dnd/idle/ users in your discord. The data is mainly used to send out alerts but why not use it for graphs as well!
        - Has two optional arguements, InputDate and Days. InputDate defaults to todays date and days (to include in graph) defaults to 1. 
    - /stream-stats Shows total time streamed for the week, two weeks, and four weeks for each platform.
- Anonymous questions/confessions
    - /confess - unlogged and anonymous confession that a user can post to a channel via the bot. Must be reviewed first
    - /confess-review - whitelisted roles/people can review submitted confessions and approve or deny them. 
        - approved confessions/questions are posted to a preset channel immediately

### How to set up the bot:

1. Go to https://discord.com/developers and set up an app and get a token. Put that token in a file called token (no file extension needed), and put that file in a subfolder called secrets.
2. At https://discord.com/developers/ - generate an invite code under oauth2 to invite your bot to your server. Under scope make sure bot is checked, and maybe commands?
    Give the bot permissions you want it to have. At minimum it'll need to be able to post messages
3. Go to the bot section in the developers portal and turn on all the intents.
4. In the Constants.py file, change the GUILD_ID value to the guild id of your server, and each platform NOTIFICATION_CHANNEL_ID to the channel ID you want alerts posted to.
    To easily get both of these IDs, in discord advanced options turn on developer mode. After that you can right click servers/channels and a new option to copy the IDs will be available.
    Also edit and add vairus URLs to your streamer in Constants.py. Everything is described in comments.
5. Make sure you have python 3.10 or better installed.
    - make sure you have chrome and chromedriver installed
    - run command 'pip install -r requirements.txt'
6. Generate the database with 'python GenerateDatabase.py' or 'python3 GenerateDatabase.py' 
7. Replace images in the image folder with those of your streamer, but keep same file names.
    - images/errIcon.png - icon used for embeds if there is an issue getting one from the platform, or if one doesn't exist
    - images/twitErrImg.jpg - default photo used for embeds if no other thumbnail or photo can be grabbed from the image list (if its empty)
    - images/avatars/calmStreamer.png - Bot avatar if streamer has streamed within the MIN_TIME_BEFORE_AVATAR_CHANGE time frame (default 48 hours)
    - images/avatars/pissedStreamer.png - Bot avatar if streamer hasn't streamed within the MIN_TIME_BEFORE_AVATAR_CHANGE time frame
8. Start the server: 'python3 run.py' or 'python run.py'

### Known Issues

1. If multiple accounts are streaming on the same platform at the same time, /rebroadcast will only show an announcement for one of the accounts.
2. Cam4 api may lock you out after a certain number of calls. May need to switch methods in the future.

### Update History
-5/03/2024 
    - Added ePlay support (80% revenue share for the win)
- 12/22/2023
    - Twitch checking hopefully fixed and turned back on
- 12/16/2023
    - Temporarily disabling twitch detection until it's fixed. All channels are showing as live
- 10/04/2023
    - Implemented the ability to post anonymous confessions/questions via /confess command.
        - These are unlogged server side
        - Must be approved by a whitelisted role/person via /confess-review
    - A new package is required to be installed so install it via the command 'pip install -U -r requirements.txt' 
- 9/29/2023
    - Expanded rerun support. 
        - If a title contains a variation of rr/rerun/not live then the stream will be detected as a rerun.
            - reruns won't be announced by default, but you can turn on rerun-announcements with the /announce-rerun-toggle command
                - if ping-toggle is turned on you can also set roles to announce reruns to in constants.py
- 9/18/2023
    - /title command added. It allows you to temporarily add a custom title for a platform/username combo.
        - title and platform arguments are required and with an optional accountName argument that is required if there's more than one account for that platform
        - TEMP_TITLE_UPTIME in constants.py determines how long a temp title added via /title will be used for. Current default is 16 hours
    - fix for Kick titles with ampersands
- 9/14/2023
    - /users-graph command upgraded to include multiple days in a graph with an optional arguemnt.
- 9/12/2023
    - Alerts can now happen for multiple accounts on the same platform at the same time.
- 9/09/2023
    - Stream-status bug fix that was causing it to give strange values and not record data
    - Can mention other roles other than everyone and each platform can get their own custom mentions
    - everyone-ping-toggle renamed to ping-toggle
    - Can now have a custom notification channel per platform if you wish
- 9/06/2023
    - Can now track multiple accounts per platform
- 9/01/2023
    - Can now add individual user IDs to command white list as well as roles. 
- 8/xx/2023
    - Added StripChat Support
    - Added BongaCams Support
    - Added MyFreeCamsSupport
    - Added Cam4 Support
