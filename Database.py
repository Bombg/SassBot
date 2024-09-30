import sqlite3
import json
import time
import datetime
from datetime import date
from datetime import timedelta
import StaticMethods

class Database:
    def __init__(self):
        pass
    
    def connectCursor(self):
        try:
            conn = sqlite3.connect("sassBot.db")
            cur = conn.cursor()
        except sqlite3.OperationalError as e:
            try:
                f = open("testingForLeak.txt", 'w')
                f.close()
            except Exception as e:
                print(e)
                if "Too many open files" in str(e):
                    print("File descriptor leak detected. Rebooting")
                    StaticMethods.rebootServer()
        return conn, cur
    
    # Confessions Table Methods
    def createConfessionsTable(self):
        conn,cur = self.connectCursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS confessions
                (
                    confession_id INTEGER PRIMARY KEY,
                    confession TEXT,
                    confession_title TEXT,
                    review_status INTEGER,
                    reviewer_id INTEGER,
                    reviewer_name TEXT,
                    date_added INTEGER,
                    date_reviewed INTEGER
                )
            ''')
        conn.commit()
        cur.close()
        conn.close()

    def addConfession(self, confession:str, title:str) -> None:
        self.createConfessionsTable()
        conn,cur = self.connectCursor()
        rowVals = (confession, title, time.time())
        exeString = f'''INSERT INTO confessions (confession,confession_title, date_added) VALUES (?,?,?)'''
        cur.execute(exeString,rowVals)
        conn.commit()
        cur.close()
        conn.close()
    
    def getUnreviewedConfession(self):
        self.createConfessionsTable()
        confessionId = 0
        confession = ""
        title = ""
        conn,cur = self.connectCursor()
        exeString = '''SELECT confession_id, confession,confession_title FROM confessions WHERE date_reviewed IS NULL LIMIT 1'''
        cur.execute(exeString)
        values = cur.fetchall()
        if values:
            confessionId = values[0][0]
            confession = values[0][1]
            title = values[0][2]
        cur.close()
        conn.close()
        self.setConfessionDateReviewed(confessionId)
        return confessionId, confession, title
    
    def setConfessionDateReviewed(self, confessionId):
        self.createConfessionsTable()
        conn, cur = self.connectCursor()
        exeString = f'''UPDATE confessions SET date_reviewed={time.time()} WHERE confession_id={confessionId} '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def reviewConfession(self, confessionId: int, approveDeny: int, reviewerId: int, reviewerName: str):
        self.createConfessionsTable()
        conn, cur = self.connectCursor()
        values = (approveDeny, reviewerId, reviewerName, time.time(), confessionId)
        exeString = f'''UPDATE confessions SET review_status=?, reviewer_id=?, reviewer_name=?, date_reviewed=? WHERE confession_id=? '''
        cur.execute(exeString,values)
        conn.commit()
        cur.close()
        conn.close()
    
    def getUnfinishedReviews(self):
        self.createConfessionsTable()
        conn, cur = self.connectCursor()
        exeString = f'''SELECT confession_id, date_reviewed FROM confessions WHERE review_status IS NULL AND date_reviewed IS NOT NULL '''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value
    
    def resetConfessionDateReviewed(self, confessionId):
        self.createConfessionsTable()
        conn, cur = self.connectCursor()
        exeString = f'''UPDATE confessions SET date_reviewed=NULL WHERE confession_id={confessionId} '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def getAllUnreviewed(self):
        self.createConfessionsTable()
        conn,cur = self.connectCursor()
        exeString = '''SELECT confession_id, confession,confession_title FROM confessions WHERE date_reviewed IS NULL'''
        cur.execute(exeString)
        values = cur.fetchall()
        cur.close()
        conn.close()
        return values
    
    # Platform_Accounts Table Methods
    def getPlatformTempTitle(self,platform, accountName):
        self.checkAddTitleCols()
        title = ""
        titleTime = 0
        conn,cur = self.connectCursor()
        exeString = f'''SELECT temp_title, temp_title_time FROM platform_accounts WHERE platform_name='{platform}' AND account_name='{accountName}' '''
        cur.execute(exeString)
        values = cur.fetchall()
        if values:
            title = values[0][0]
            titleTime = values[0][1]
        cur.close()
        conn.close()
        return title, titleTime

    def getPlatformAccountNames(self,platform:str):
        conn,cur = self.connectCursor()
        names= []
        exeString = f'''SELECT account_name FROM platform_accounts WHERE platform_name='{platform}' '''
        if self.isExists(exeString):
            cur.execute(exeString)
            namesList = cur.fetchall()
            for name in namesList:
                names.append(name[0])
        cur.close()
        conn.close()
        return names

    def doesAccountExist(self,platform, accountName):
        isExistString = f'''SELECT temp_title, temp_title_time FROM platform_accounts WHERE platform_name='{platform}' AND account_name='{accountName}' '''
        accountExist = self.isExists(isExistString)
        return accountExist

    def addTempTitle(self,title: str, platform: str, accountName: str ) -> None:
        self.createPlatformAccountsTable()
        self.checkAddTitleCols()
        conn,cur = self.connectCursor()
        if self.doesAccountExist(platform, accountName):
            exeString = f'''UPDATE platform_accounts SET temp_title='{title}', temp_title_time={time.time()} WHERE platform_name='{platform}' AND account_name='{accountName}' '''
            cur.execute(exeString)
            conn.commit()
            cur.close()
            conn.close()
        else:
            print("given bad account or platform. can't update title")

    def checkAddTitleCols(self):
        isTitleExist = self.isColExist("platform_accounts","temp_title")
        if not isTitleExist:
            conn,cur = self.connectCursor()
            cur.execute('''ALTER TABLE platform_accounts ADD temp_title TEXT ''')
            cur.execute('''ALTER TABLE platform_accounts ADD temp_title_time REAL ''')
            conn.commit()
            cur.close()
            conn.close()

    def createPlatformAccountsTable(self) -> None:
        conn,cur = self.connectCursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS platform_accounts
                (
                    account_name TEXT NOT NULL,
                    platform_name TEXT NOT NULL, 
                    last_online_message REAL,
                    last_stream_start_time REAL,
                    last_stream_end_time REAL,
                    temp_title TEXT,
                    temp_title_time REAL,
                    PRIMARY KEY (account_name, platform_name),
                    FOREIGN KEY(platform_name) REFERENCES platforms(platform_name)
                )
            ''')
        conn.commit()
        cur.close()
        conn.close()

    def createNewPlatformAccount(self, accountName:str, platformName:str,lastOnlineMessage = 0, lastStreamStartTime = 0, lastStreamEndTime = 0) -> None:
        self.createPlatformAccountsTable()
        conn,cur = self.connectCursor()
        rowVals =(accountName, platformName, lastOnlineMessage, lastStreamStartTime, lastStreamEndTime)
        cur.execute('INSERT INTO platform_accounts (account_name, platform_name, last_online_message, last_stream_start_time, last_stream_end_time) VALUES (?,?,?,?,?)',rowVals)
        conn.commit()
        cur.close()
        conn.close()

    def getPlatformAccountsRowValues(self, platformName, accountName):
        self.createPlatformAccountsTable()
        conn,cur = self.connectCursor()
        exeString = f'''SELECT last_online_message,last_stream_start_time,last_stream_end_time FROM platform_accounts WHERE platform_name='{platformName}' AND account_name='{accountName}' '''
        if not self.isExists(exeString):
            self.createNewPlatformAccount(accountName, platformName)
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value[0][0],value[0][1],value[0][2]
    
    def updatePlatformAccountRowCol(self,platformName,accountName,col,newValue):
        self.createPlatformAccountsTable()
        conn,cur = self.connectCursor()
        exeString = f'''UPDATE platform_accounts SET {col}={newValue} WHERE platform_name='{platformName}' AND account_name='{accountName}' '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    # Platform Table Methods
    def setRerun(self, isRerun, platform):
        self.checkAddRerunCols()
        conn,cur = self.connectCursor()
        tFalse = 1 if isRerun else 0
        exeString = f'''UPDATE platforms SET rerun_playing={tFalse} WHERE platform_name='{platform}' '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()

    def getRerun(self, platform):
        isRerun = 0
        self.checkAddRerunCols()
        conn, cur = self.connectCursor()
        exeString = f'''SELECT rerun_playing FROM platforms WHERE platform_name='{platform}' '''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        if value[0][0] != None:
            isRerun = value[0][0]
        return isRerun

    def updatePlatformRowCol(self,rowKey,col,newValue):
        conn,cur = self.connectCursor()
        exeString = f'''UPDATE platforms SET {col}={newValue} WHERE platform_name='{rowKey}' '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()

    def getPlatformsRowCol(self, rowKey, col):
        conn,cur = self.connectCursor()
        exeString = f'''SELECT {col} FROM platforms WHERE platform_name='{rowKey}' '''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value[0][0]
    
    def getPlatformsRowValues(self, platformName):
        self.checkAddPlatformRow(platformName)
        conn,cur = self.connectCursor()
        exeString = f'''SELECT last_online_message,last_stream_start_time,last_stream_end_time FROM platforms WHERE platform_name='{platformName}' '''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        isRerun = self.getRerun(platformName)
        return value[0][0],value[0][1],value[0][2], isRerun
    
    def checkAddPlatformRow(self,platformName):
        exeString = f'''SELECT * FROM platforms WHERE platform_name='{platformName}' '''
        isExists = self.isExists(exeString)
        if not isExists:
            conn,cur = self.connectCursor()
            rowVals =(platformName,0,0,0)
            cur.execute('INSERT INTO platforms (platform_name, last_online_message,last_stream_start_time,last_stream_end_time) VALUES (?,?,?,?)',rowVals)
            conn.commit()
            cur.close()
            conn.close()
    
    # Subathon Table Methods
    def startSubathon(self,epochTime):
        conn,cur = self.connectCursor()
        subTrue = 1
        exeString = f'''UPDATE subathon SET subathon={subTrue}, start_time={epochTime}  '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()

    def endSubathon(self,epochTime):
        conn,cur = self.connectCursor()
        subFalse = 0
        exeString = f'''UPDATE subathon SET subathon={subFalse}, end_time={epochTime}  '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()

    def getSubathonStatus(self):
        conn,cur = self.connectCursor()
        exeString = f'''SELECT subathon,start_time,end_time FROM subathon'''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value[0]
    
    def getSubathonStatusClean(self):
        sub = self.getSubathonStatus()
        subathon = sub[0]
        subStart = sub[1]
        subEnd = sub[2]
        return subathon,subStart,subEnd
    
    def getSubathonLongest(self):
        conn,cur = self.connectCursor()
        exeString = f'''SELECT longest_subathon FROM subathon'''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value[0][0]
    
    def getSubathonLongestTime(self):
        conn,cur = self.connectCursor()
        exeString = f'''SELECT longest_subathon,longest_subathon_time FROM subathon'''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value[0][0],value[0][1]
    
    def setLongestSubathon(self,subathonLength,subathonStartTime):
        conn,cur = self.connectCursor()
        exeString = f'''UPDATE subathon SET longest_subathon={subathonLength},longest_subathon_time={subathonStartTime}  '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()

    # Stream Table Methods
    def setRerunAnnounce(self, isAnnounce):
        self.checkAddRerunCols()
        conn,cur = self.connectCursor()
        tFalse = 1 if isAnnounce else 0
        exeString = f'''UPDATE stream SET rerun_ping={tFalse}'''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def getRerunAnnounce(self):
        isRerun = 0
        self.checkAddRerunCols()
        conn, cur = self.connectCursor()
        exeString = f'''SELECT rerun_ping FROM stream '''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        if value[0][0] != None:
            isRerun = value[0][0]
        return isRerun

    def getStreamTableValues(self):
        conn,cur = self.connectCursor()
        exeString = f'''SELECT last_online,last_offline,last_stream_length FROM stream'''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value[0][0],value[0][1],value[0][2]
    
    def setStreamLastOnline(self,lastOnline):
        conn,cur = self.connectCursor()
        exeString = f'''UPDATE stream SET last_online={lastOnline} '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def setStreamLastOffline(self,lastOffline):
        conn,cur = self.connectCursor()
        exeString = f'''UPDATE stream SET last_offline={lastOffline} '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def setStreamLastStreamLength(self,lastStreamLength):
        conn,cur = self.connectCursor()
        exeString = f'''UPDATE stream SET last_stream_length={lastStreamLength} '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def getTwImgStuff(self):
        conn,cur = self.connectCursor()
        exeString = f'''SELECT tw_img_list,tw_img_queue, img_banned_list FROM stream'''
        cur.execute(exeString)
        value = cur.fetchall()
        if value[0][2] is None:
            bannedList = []
        else:
            bannedList = json.loads(value[0][2])
        if value[0][0] is None or value[0][1] is None:
            twImgList = []
            twImgQue =[]
        else:
            twImgList = json.loads(value[0][0])
            twImgQue = json.loads(value[0][1])
        cur.close()
        conn.close()
        return twImgList, twImgQue, bannedList
    
    def setBannedList(self, bannedList):
        conn,cur = self.connectCursor()
        bannedListDump = json.dumps(bannedList)
        exeString = f'''UPDATE stream SET img_banned_list='{bannedListDump}' '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def setTwImgList(self,twImgList):
        conn,cur = self.connectCursor()
        twImgListDump = json.dumps(twImgList)
        exeString = f'''UPDATE stream SET tw_img_list='{twImgListDump}' '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def setTwImgQueue(self,twImgQueue):
        conn,cur = self.connectCursor()
        twImgQueueDump = json.dumps(twImgQueue)
        exeString = f'''UPDATE stream SET tw_img_queue='{twImgQueueDump}' '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()

    def setImgPin(self, epochTime: int, url: str) -> None:
        conn,cur = self.connectCursor()
        exeString = f'''UPDATE stream SET img_pin={epochTime}, img_pin_url='{url}' '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def getImgPin(self):
        conn,cur = self.connectCursor()
        exeString = f'''SELECT img_pin, img_pin_url FROM stream '''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value[0][0],value[0][1]
    
    def getPing(self):
        conn,cur = self.connectCursor()
        exeString = f'''SELECT everyone_ping FROM stream '''
        cur.execute(exeString)
        value = cur.fetchall()
        ping = False
        if value[0][0]:
            ping = True
        cur.close()
        conn.close()
        return ping
    
    def setPing(self, ifPing: bool) -> None:
        conn,cur = self.connectCursor()
        ping = 1 if ifPing else 0
        exeString = f'''UPDATE stream SET everyone_ping={ping} '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    # User_Presence_Stats Table Methods
    def isPresDateExists(self, dataDate: date) -> bool:
        exeString = f'''SELECT user_presences FROM user_presence_stats WHERE date='{dataDate}' '''
        isExists = self.isExists(exeString)
        return isExists
    
    def getPresenceDay(self,dataDate: date) -> dict:
        conn,cur = self.connectCursor()
        presenceDict = {}
        exeString = f'''SELECT user_presences FROM user_presence_stats WHERE date='{dataDate}' '''
        if self.isExists(exeString):
            cur.execute(exeString)
            value = cur.fetchall()
            presenceDict = json.loads(value[0][0])
        elif str(dataDate) == str(date.today()):
            for i in range(144):
                hour = int(i/6)
                minute = i%6
                minute = minute * 10
                hourMinute = f'{hour}:{minute}'
                presenceDict[hourMinute] = 0
            self.setNewPresenceDay(date.today(),datetime.datetime.now().weekday(),presenceDict)
        cur.close()
        conn.close()
        return presenceDict
    
    def setPresenceDay(self, dataDate: date, presenceDict: dict) -> None:
        conn,cur = self.connectCursor()
        presenceDictDump = json.dumps(presenceDict)
        exeString = f'''UPDATE user_presence_stats SET user_presences='{presenceDictDump}' WHERE date = '{dataDate}' '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()

    def setNewPresenceDay(self, dataDate: date, dataWeekDay: int, presenceDict: dict) -> None:
        conn,cur = self.connectCursor()
        presenceDictDump = json.dumps(presenceDict)
        rowVals =(dataDate, dataWeekDay, presenceDictDump)
        cur.execute('INSERT INTO user_presence_stats (date, week_day, user_presences) VALUES (?,?,?)',rowVals)
        conn.commit()
        cur.close()
        conn.close()

    def getLastWeeksDayPresenceData(self, dayDate: date) -> dict:
        conn,cur = self.connectCursor()
        previousWeekDayDate = dayDate - timedelta(days = 7)
        value = 0
        lastWeekPres = self.getPresenceDay(previousWeekDayDate)
        if lastWeekPres:
            value = lastWeekPres
        cur.close()
        conn.close()
        return value
    
    # Helper Functions
    def isExists(self,query: str) -> bool:
        conn,cur = self.connectCursor()
        exists = f"SELECT EXISTS({query})"
        isExists = False
        try:
            cur.execute(exists)
            value = cur.fetchall()
            isExists = value[0][0]
        except sqlite3.OperationalError:
            print("error when checking if col exists, perhaps no data yet")
        cur.close()
        conn.close()
        return isExists
    
    def isColExist(self,tableName, colName):
        isExist = False
        conn,cur = self.connectCursor()
        cur.execute(f'PRAGMA table_info({tableName})')
        retCols = cur.fetchall()
        for col in retCols:
            if colName in col:
                isExist = True
        cur.close()
        conn.close()
        return isExist
    
    def checkAddRerunCols(self):
        isTitleExist = self.isColExist("stream","rerun_ping")
        if not isTitleExist:
            conn,cur = self.connectCursor()
            cur.execute('''ALTER TABLE stream ADD rerun_ping INTEGER ''')
            cur.execute('''ALTER TABLE platforms ADD rerun_playing INTEGER ''')
            conn.commit()
            cur.close()
            conn.close()