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
### Features
- Get notifications when your streamer is online sent to a discord channel
- If twitch/kick title contains a variation of rerun/rr/not live then a notification will not be sent
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
- /everyone-ping-toggle - Toggle for @everyone pings in the announcements channel
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
    - /stream-stats Shows total time streamed for the week, two weeks, and four weeks for each platform.

### How to set up the bot:

1. Go to https://discord.com/developers and set up an app and get a token. Put that token in a file called token (no file extension needed), and put that file in a subfolder called secrets.
2. At https://discord.com/developers/ - generate an invite code under oauth2 to invite your bot to your server. Under scope make sure bot is checked, and maybe commands?
    Give the bot permissions you want it to have. At minimum it'll need to be able to post messages
3. Go to the bot section in the developers portal and turn on all the intents.
4. In the Constants.py file, change the GUILD_ID value to the guild id of your server, and STDOUT_CHANNEL_ID to the channel ID you want alerts posted to.
    To easily get both of these IDs, in discord advanced options turn on developer mode. After that you can right click servers/channels and a new option to copy the IDs will be available.
    Also edit and add vairus URLs to your streamer in Constants.py. Everything is described in comments.
5. Make sure you have python 3.10 or better installed.
    run command 'pip install -r requirements.txt'
6. Generate the database with 'python GenerateDatabase.py' or 'python3 GenerateDatabase.py' 
7. Replace images in the image folder with those of your streamer, but keep same file names.
    - images/errIcon.png - icon used for embeds if there is an issue getting one from the platform, or if one doesn't exist
    - images/twitErrImg.jpg - default photo used for embeds if no other thumbnail or photo can be grabbed.
    - images/avatars/calmStreamer.png - Bot avatar if streamer has streamed within the MIN_TIME_BEFORE_AVATAR_CHANGE time frame (default 48 hours)
    - images/avatars/pissedStreamer.png - Bot avatar if streamer hasn't streamed within the MIN_TIME_BEFORE_AVATAR_CHANGE time frame
8. Start the server: 'python3 run.py' or 'python run.py'