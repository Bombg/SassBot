from utils.Database import Database
import matplotlib.pyplot as plt
import os
from DefaultConstants import Settings as Settings
from datetime import datetime
from datetime import timedelta
import requests
from matplotlib.gridspec import GridSpec

baseSettings = Settings()

def createUserDayGraph(inputDate: str, days = 1) -> None:
    db = Database()
    inputDate = datetime.strptime(inputDate, '%Y-%m-%d').date()
    lastWeekPresencesDict = db.getLastWeeksDayPresenceData(inputDate)
    presencesDict = {}
    for i in reversed(range(days)):
        previousDate = inputDate - timedelta(days = i)
        previousDateDict = db.getPresenceDay(previousDate)
        for k, v in previousDateDict.items():
            key = str(previousDate.day)+"-" + k if days > 1 else k
            presencesDict[key] = v
    x, yTotalUsers, yDnd, yOnline, yIdle = getTodaysLists(presencesDict)
    yTotalUsersLastWeek = getLastWeekList(lastWeekPresencesDict, x)
    totalMembers = addTotalMembers(presencesDict)
    plt.figure(figsize=(15, 5))
    plt.xticks(rotation='vertical')
    if lastWeekPresencesDict and days  == 1: 
        plt.plot(x,yTotalUsersLastWeek, label = "Total users(same day last week)", color = "cyan")
    plt.plot(x,yTotalUsers, label = "Total users(logged in to discord)", color = "blue")
    plt.plot(x,yDnd, label ="dnd", color = 'red')
    plt.plot(x,yOnline, label = "online", color = "green")
    plt.plot(x, yIdle, label = "idle", color = "orange")
    addOnlineCols(presencesDict)
    plt.legend(bbox_to_anchor=(1.075, 1.0), loc='upper left')
    xlabel = "Time(D-HH:MM)" if days > 1 else "Time"
    plt.xlabel(xlabel)
    plt.ylabel("Users")
    title = str(inputDate - timedelta(days = days - 1)) + " to " + str(inputDate) if days > 1 else inputDate
    plt.title(title)
    ax = plt.gca()
    hideLabelsAndTicks(ax,days)
    plotSecondYAxis(x, totalMembers, ax)
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    plt.tight_layout()
    path = f"graphs/{title}.png"
    plt.savefig(path)
    return path

def plotSecondYAxis(x, totalMembers, ax):
    ax2 = ax.twinx()
    ax2.plot(x,totalMembers, color = "violet", label = "All members(offline and online)")
    ax2.set_ylabel("All members", color = "violet")
    ax2.legend(bbox_to_anchor=(1.075, 0.4), loc='upper left')
    ax2.tick_params(axis='y', labelcolor="violet")

def hideLabelsAndTicks(ax, days):
    labelsToHide = ax.xaxis.get_ticklabels()
    ticksToHide = ax.xaxis.get_major_ticks()
    stepSize = 6 * days
    labelsToHide = list(set(labelsToHide) - set(labelsToHide[::stepSize])) #x[:a:b:c] - list slicing - a is the starting index, b is the ending index and c is the optional step size. 
    for label in labelsToHide:                                             #L[x::y] means a slice of L where the x is the index to start from and y is the step size. 
        label.set_visible(False)                                           #temp[::6] means every 6th element from temp. temp = del temp[::6] the same thing?
    ticksToHide = list(set(ticksToHide) - set(ticksToHide[::stepSize]))
    for tick in ticksToHide:
        tick.set_visible(False)

def addTotalMembers(presencesDict: dict):
    totalMembers = []
    for k, v in presencesDict.items():
        if v:
            if 'members' in v.keys():
                totalMembers.append(v['members'])
            else:
                totalMembers.append(None)
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
                        plt.axvspan(k, nextkey, facecolor=newFaceColor, alpha=0.25,zorder=3, label = baseSettings.streamerName + " Streaming " + v['streaming'] )
                        labels.append(newFaceColor)
                    else:
                        plt.axvspan(k, nextkey, facecolor=newFaceColor, alpha=0.25,zorder=3)
                except (ValueError, IndexError):
                    pass

def getFaceColor(streamingValues: str):
    faceColor = 'g'
    if 'RR' in streamingValues:
        faceColor = '#808080'
    elif 'Kick' in streamingValues:
        faceColor = "g"
    elif "OF" in streamingValues:
        faceColor = baseSettings.ofEmbedColor
    elif "Fans" in streamingValues:
        faceColor = baseSettings.fansEmbedColor
    elif "CB" in streamingValues:
        faceColor = baseSettings.cbEmbedColor
    elif "YT" in streamingValues:
        faceColor = baseSettings.ytEmbedColor
    elif "Twitch" in streamingValues:
        faceColor = baseSettings.ytEmbedColor
    elif "Cam4" in streamingValues:
        faceColor = baseSettings.cam4EmbedColor
    elif "MFC" in streamingValues:
        faceColor = baseSettings.mfcEmbedColor
    elif "BC" in streamingValues:
        faceColor = baseSettings.bcEmbedColor
    elif "SC" in streamingValues:
        faceColor = baseSettings.scEmbedColor
    elif "EP" in streamingValues:
        faceColor = baseSettings.epEmbedColor
    elif "MV" in streamingValues:
        faceColor = baseSettings.mvEmbedColor
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
        x.append(str(k))
        if v:
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
        else:
            yTotalUsers.append(None)
            yDnd.append(None)
            yOnline.append(None)
            yIdle.append(None)
    return x,yTotalUsers,yDnd,yOnline,yIdle

def GetEmoteStatsImage(prefix, days):
    db = Database()
    emoteNames, images, numbers = db.GetAllKickEmotesWithPrefix(prefix, days)
    i = 0
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    for image in  images:
        response = requests.get(image)
        if response.status_code == 200:
            fileName = f"graphs/testImg{i}.jpg"
            f = open(fileName, "wb")
            f.write(response.content)
            f.close()
            images[i] = fileName
            i += 1
    
    fig = plt.figure(figsize=(4, len(emoteNames) * .5))
    gs = GridSpec(nrows=len(images), ncols=3, width_ratios=[1, 1, 1],wspace=0.1, hspace=0.1)
    for i in range(len(images)):
        # --- Column 1: Title ---
        axTitle = fig.add_subplot(gs[i, 0])
        axTitle.text(0.5, 0.5, emoteNames[i], ha='center', va='center', fontsize=8)
        axTitle.axis('off') 

        # --- Column 2: Image ---
        ax_img = fig.add_subplot(gs[i, 1])
        try:
            with open(images[i], 'rb') as f:
                img = plt.imread(f)
            ax_img.imshow(img)
        except Exception as e:
            ax_img.text(0.5, 0.5, 'Image not found', ha='center', va='center')
            print(f"Could not load image {images[i]}: {e}")
        ax_img.axis('off')

        # --- Column 3: Number ---
        ax_num = fig.add_subplot(gs[i, 2])
        ax_num.text(0.5, 0.5, str(numbers[i]), ha='center', va='center', fontsize=24)
        ax_num.axis('off')
    
    plt.tight_layout()
    path = "graphs/emoteStats.png"
    plt.savefig(path)
    return path