from Database import Database
import matplotlib.pyplot as plt
import os

def createUserDayGraph(date: str) -> None:
    db = Database()
    yyyyDashMmDashDd = date
    presencesDict = db.getPresenceDay(yyyyDashMmDashDd)
    x = []
    y = []
    for k, v in presencesDict.items():
        if v:
            x.append(k)
            newVal = 0
            for keys, vals in v.items():
                newVal += vals
            y.append(newVal)
    plt.figure(figsize=(15, 4))
    plt.plot(x,y)
    ax = plt.gca()
    temp = ax.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::6]))
    for label in temp:
        label.set_visible(False)
    if not os.path.exists("graphs"):
        os.makedirs("graphs")    
    plt.savefig(f"graphs/{yyyyDashMmDashDd}.png")