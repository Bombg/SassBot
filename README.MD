How to set up the bot:

1. Go to https://discord.com/developers and set up an app and get a token. Put that token in a file called token (no file extension needed), and put that file in a subfolder called secrets.
2. At https://discord.com/developers/ - generate an invite code to invite your bot to your server. Under scope make sure bot is checked, and maybe commands?
    Give the bot permissions you want it to have. At minimum it'll need to be able to post messages
3. In the Constants.py file, change the GUILD_ID value to the guild id of your server, and STDOUT_CHANNEL_ID to the channel ID you want alerts posted to.
    To easily get both of these IDs, in discord advanced options turn on developer mode. After that you can right click servers/channels and a new option to copy the IDs will be available
4. Make sure you have python 3.10 or better installed.
    run command 'pip install -r requirements.txt'
5. Start the server: 'python3 run.py' or 'python run.py'