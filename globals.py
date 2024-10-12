try:
    from AppConstants import Constants as Constants
except ImportError:
    from DefaultConstants import Constants as Constants
import time

globalPlayString = ""
normalAvtar = False

botStartTime = time.time()

rebroadcast = {
    "chaturbate":0,
    "onlyfans":0,
    "fansly":0,
    "twitch":0,
    "youtube":0,
    "kick":0,
    "cam4":0,
    "mfc":0,
    "bongacams":0,
    "stripchat":0,
    "eplay":0
}

confessionIds = {"alert":0}

browserOpen = False