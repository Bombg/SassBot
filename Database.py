import sqlite3
import json
import time
import datetime
from datetime import date

class Database:
    def __init__(self):
        pass
    
    def updateTableRowCol(self,table,rowKey,col,newValue):
        conn,cur = self.connectCursor()
        exeString = f'''UPDATE {table} SET {col}={newValue} WHERE platform_name='{rowKey}' '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()

    def getTableRowCol(self,table, rowKey, col):
        conn,cur = self.connectCursor()
        exeString = f'''SELECT {col} FROM {table} WHERE platform_name='{rowKey}' '''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value[0][0]

    def connectCursor(self):
        conn = sqlite3.connect("cassBot.db")
        cur = conn.cursor()
        return conn, cur
    
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

    def getPlatformsRowValues(self, platformName):
        conn,cur = self.connectCursor()
        exeString = f'''SELECT last_online_message,last_stream_start_time,last_stream_end_time FROM platforms WHERE platform_name='{platformName}' '''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value[0][0],value[0][1],value[0][2]

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
    
    def isExists(self,query: str) -> bool:
        conn,cur = self.connectCursor()
        exists = f"SELECT EXISTS({query})"
        cur.execute(exists)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value[0][0]
    
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

    def getLastWeeksDayPresenceData(self) -> dict:
        conn,cur = self.connectCursor()
        weekday = datetime.datetime.now().weekday()
        yesterdayWeekDay = (datetime.datetime.now().weekday() + 6) % 7
        today = str(date.today())
        value = 0
        weekAgoQuery = f'SELECT date, week_day, user_presences FROM user_presence_stats WHERE week_day={weekday} EXCEPT SELECT date, week_day, user_presences FROM user_presence_stats WHERE date = \'{today}\' ORDER BY date DESC LIMIT 1'
        yesterdayQuery = f'SELECT date, week_day, user_presences FROM user_presence_stats WHERE week_day={yesterdayWeekDay} ORDER BY date DESC LIMIT 1'
        if self.isExists(weekAgoQuery):
            cur.execute(weekAgoQuery)
            value = cur.fetchall()
            value = json.loads(value[0][2])
        elif self.isExists(yesterdayQuery):
            cur.execute(yesterdayQuery)
            value = cur.fetchall()
            value = json.loads(value[0][2])
        cur.close()
        conn.close()
        return value

    