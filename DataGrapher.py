from Database import Database
import matplotlib.pyplot as plt
import os
from datetime import date
from Constants import Constants
from datetime import datetime

def createUserDayGraph(inputDate: str) -> None:
    db = Database()
    inputDate = datetime.strptime(inputDate, '%Y-%m-%d').date()
    presencesDict = db.getPresenceDay(inputDate)
    lastWeekPresencesDict = db.getLastWeeksDayPresenceData(inputDate)
    x, yTotalUsers, yDnd, yOnline, yIdle = getTodaysLists(presencesDict)
    yTotalUsersLastWeek = getLastWeekList(lastWeekPresencesDict, x)
    totalMembers = addTotalMembers(presencesDict)
    plt.figure(figsize=(15, 5))
    if lastWeekPresencesDict: 
        plt.plot(x,yTotalUsersLastWeek, label = "Total users(same day last week)", color = "cyan")
    plt.plot(x,yTotalUsers, label = "Total users(logged in to discord)", color = "blue")
    plt.plot(x,yDnd, label ="dnd", color = 'red')
    plt.plot(x,yOnline, label = "online", color = "green")
    plt.plot(x, yIdle, label = "idle", color = "orange")
    addOnlineCols(presencesDict)
    plt.legend(bbox_to_anchor=(1.075, 1.0), loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Users")
    plt.title(str(inputDate))
    ax = plt.gca()
    hideLabels(ax)
    plotSecondYAxis(x, totalMembers, ax)
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    plt.tight_layout()    
    plt.savefig(f"graphs/{inputDate}.png")

def plotSecondYAxis(x, totalMembers, ax):
    ax2 = ax.twinx()
    ax2.plot(x,totalMembers, color = "violet", label = "All members(offline and online)")
    ax2.set_ylabel("All members", color = "violet")
    ax2.legend(bbox_to_anchor=(1.075, 0.4), loc='upper left')
    ax2.tick_params(axis='y', labelcolor="violet")

def hideLabels(ax):
    temp = ax.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::6])) #x[:a:b:c] - list slicing - a is the starting index, b is the ending index and c is the optional step size. 
    for label in temp:                      #L[x::y] means a slice of L where the x is the index to start from and y is the step size. 
        label.set_visible(False)            #temp[::6] means every 6th element from temp. temp = del temp[::6] the same thing?

def addTotalMembers(presencesDict: dict):
    totalMembers = []
    for k, v in presencesDict.items():
        if v:
            if 'members' in v.keys():
                totalMembers.append(v['members'])
            else:
                totalMembers.append(None)
    return totalMembers

def addOnlineCols(presencesDict):
    dictKeys = list(presencesDict)
    labels = []
    for k, v in presencesDict.items():
        if v:
            if 'streaming' in v.keys():
                try:
                    newFaceColor = getFaceColor(v['streaming'])
                    nextkey = dictKeys[dictKeys.index(k) + 1]
                    if newFaceColor not in labels:
                        plt.axvspan(k, nextkey, facecolor=newFaceColor, alpha=0.25,zorder=3, label = Constants.streamerName + " Streaming " + v['streaming'] )
                        labels.append(newFaceColor)
                    else:
                        plt.axvspan(k, nextkey, facecolor=newFaceColor, alpha=0.25,zorder=3)
                except (ValueError, IndexError):
                    pass

def getFaceColor(streamingValues: str):
    faceColor = 'g'
    if 'Kick' in streamingValues:
        faceColor = "g"
    elif "OF" in streamingValues:
        faceColor = Constants.ofEmbedColor
    elif "Fans" in streamingValues:
        faceColor = Constants.fansEmbedColor
    elif "CB" in streamingValues:
        faceColor = Constants.cbEmbedColor
    elif "YT" in streamingValues:
        faceColor = Constants.ytEmbedColor
    elif "Twitch" in streamingValues:
        faceColor = Constants.ytEmbedColor
    elif "Cam4" in streamingValues:
        faceColor = Constants.cam4EmbedColor
    elif "MFC" in streamingValues:
        faceColor = Constants.mfcEmbedColor
    elif "BC" in streamingValues:
        faceColor = Constants.bcEmbedColor
    elif "SC" in streamingValues:
        faceColor = Constants.scEmbedColor
    return faceColor

def getLastWeekList(lastWeekPresencesDict, x):
    yTotalUsersLastWeek = []
    if lastWeekPresencesDict:
        for k, v in lastWeekPresencesDict.items():
            if v:
                if k in x:
                    totalUsers = 0
                    for ke, va in v.items():
                        if isinstance(va,int) and ke != 'members':
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
                if isinstance(vals,int) and keys != 'members':
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