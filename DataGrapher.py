from Database import Database
import matplotlib.pyplot as plt
import os

def createUserDayGraph(date: str) -> None:
    db = Database()
    yyyyDashMmDashDd = date
    presencesDict = db.getPresenceDay(yyyyDashMmDashDd)
    x = []
    yTotalUsers = []
    yDnd = []
    yOnline = []
    yIdle = []
    for k, v in presencesDict.items():
        if v:
            x.append(k)
            totalUsers = 0
            dnd = 0
            online = 0
            idle = 0
            for keys, vals in v.items():
                totalUsers += vals
                if keys == 'dnd':
                    dnd += vals
                elif keys == 'online':
                    online += vals
                elif keys == 'idle':
                    idle += vals
            yTotalUsers.append(totalUsers)
            yDnd.append(dnd)
            yOnline.append(online)
            yIdle.append(idle)
    plt.figure(figsize=(15, 5))
    plt.plot(x,yTotalUsers, label = "Total users(logged in to discord)")
    plt.plot(x,yDnd, label ="dnd", color = 'red')
    plt.plot(x,yOnline, label = "online", color = "green")
    plt.plot(x, yIdle, label = "idle", color = "orange")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    ax = plt.gca()
    temp = ax.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::6]))
    for label in temp:
        label.set_visible(False)
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    plt.tight_layout()    
    plt.savefig(f"graphs/{yyyyDashMmDashDd}.png")