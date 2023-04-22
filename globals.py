from Constants import Constants
import time

WAIT_BETWEEN_MESSAGES = Constants.WAIT_BETWEEN_MESSAGES
chaturFalse = WAIT_BETWEEN_MESSAGES
onlyFalse = WAIT_BETWEEN_MESSAGES
fansFalse = WAIT_BETWEEN_MESSAGES
twitchFalse = WAIT_BETWEEN_MESSAGES
ytFalse = WAIT_BETWEEN_MESSAGES
kickFalse = WAIT_BETWEEN_MESSAGES
kittiesKickFalse = WAIT_BETWEEN_MESSAGES

chaturLastOnlineMessage = 0
onlyLastOnlineMessage = 0
fansLastOnlineMessage = 0
twitchLastOnlineMessage = 0
ytLastOnlineMessage = 0
kickLastOnlineMessage = 0
kittiesKickLastOnlineMessage = 0

globalPlayString = ""
online = False
offTime = 0
onTime = 0
totalOnTime = 0
normalAvtar = False

subathon = False
subathonStartTime = 0
subathonEndTime = 0

botStartTime = time.time()