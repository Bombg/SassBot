import sqlite3

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