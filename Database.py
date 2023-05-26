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
