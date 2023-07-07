from Database import Database
import matplotlib.pyplot as plt
import os
from datetime import date
from Constants import Constants

def createUserDayGraph(inputDate: str) -> None:
    db = Database()
    yyyyDashMmDashDd = inputDate
    presencesDict = db.getPresenceDay(yyyyDashMmDashDd)
    lastWeekPresencesDict = db.getLastWeeksDayPresenceData()
    x, yTotalUsers, yDnd, yOnline, yIdle = getTodaysLists(presencesDict)
    yTotalUsersLastWeek = getLastWeekList(lastWeekPresencesDict, x)
    plt.figure(figsize=(15, 5))
    if lastWeekPresencesDict and str(date.today()) == yyyyDashMmDashDd: 
        plt.plot(x,yTotalUsersLastWeek, label = "Total users(same day last week)", color = "cyan")
    plt.plot(x,yTotalUsers, label = "Total users(logged in to discord)", color = "blue")
    plt.plot(x,yDnd, label ="dnd", color = 'red')
    plt.plot(x,yOnline, label = "online", color = "green")
    plt.plot(x, yIdle, label = "idle", color = "orange")
    addOnlineCols(presencesDict)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Users")
    plt.title(str(inputDate))
    ax = plt.gca()
    temp = ax.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::6]))
    for label in temp:
        label.set_visible(False)
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    plt.tight_layout()    
    plt.savefig(f"graphs/{yyyyDashMmDashDd}.png")

def addOnlineCols(presencesDict):
    dictKeys = list(presencesDict)
    label = False
    for k, v in presencesDict.items():
        if v:
            if 'streaming' in v.keys():
                try:
                    nextkey = dictKeys[dictKeys.index(k) + 1]
                    if not label:
                        plt.axvspan(k, nextkey, facecolor='g', alpha=0.25,zorder=3, label = Constants.streamerName + " Streaming")
                        label = True
                    else:
                        plt.axvspan(k, nextkey, facecolor='g', alpha=0.25,zorder=3)
                except (ValueError, IndexError):
                    pass

def getLastWeekList(lastWeekPresencesDict, x):
    yTotalUsersLastWeek = []
    if lastWeekPresencesDict:
        for k, v in lastWeekPresencesDict.items():
            if v:
                if k in x:
                    totalUsers = 0
                    for ke, va in v.items():
                        totalUsers += va
                    yTotalUsersLastWeek.append(totalUsers)
            elif k in x:
                yTotalUsersLastWeek.append(None)
    return yTotalUsersLastWeek

def getTodaysLists(presencesDict):
    x = []
    yTotalUsers = []
    yDnd = []
    yOnline = []
    yIdle = []
    for k, v in presencesDict.items():
        if v:
            x.append(str(k))
            totalUsers = 0
            dnd = 0
            online = 0
            idle = 0
            for keys, vals in v.items():
                if isinstance(vals,int):
                    totalUsers += vals
                if keys == 'dnd':
                    dnd += vals
                elif keys == 'online':
                    online += vals
                elif keys == 'idle':
                    idle += vals
            yTotalUsers.append(int(totalUsers))
            yDnd.append(int(dnd))
            yOnline.append(int(online))
            yIdle.append(int(idle))
    return x,yTotalUsers,yDnd,yOnline,yIdle