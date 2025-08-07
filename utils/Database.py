import sqlite3
import json
import time
import datetime
from datetime import date
from datetime import timedelta
import utils.StaticMethods as StaticMethods
import logging
from DefaultConstants import Settings as Settings
import GenerateDatabase
import os
import re

baseSettings = Settings()

class Database:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(baseSettings.SASSBOT_LOG_LEVEL)
    
    def connectCursor(self):
        try:
            if not os.path.exists("sassBot.db"):
                GenerateDatabase.GenerateDatabase()
            conn = sqlite3.connect("sassBot.db")
            cur = conn.cursor()
        except sqlite3.OperationalError as e:
            try:
                f = open("testingForLeak.txt", 'w')
                f.close()
            except Exception as e:
                self.logger.error(e)
                if "Too many open files" in str(e):
                    self.logger.critical("File descriptor leak detected. Rebooting")
                    StaticMethods.rebootServer()
        return conn, cur
    
    def GetKickSlugFromId(self, kickId):
        slug = ""
        self.createKickUserTable()
        conn, cur = self.connectCursor()
        rowVals = (kickId,)
        exeString = '''SELECT slug FROM kick_users WHERE id=?'''
        cur.execute(exeString, rowVals)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            slug = fetch[0][0]
        cur.close()
        conn.close()
        return slug
    
    def GetAllKickEmotesWithPrefix(self, emotePrefix:str, days:int):
        emoteList = {}
        urls = {}
        self.createKickChatTable()
        conn, cur = self.connectCursor()
        exeString = '''SELECT content, date FROM kick_chat ORDER BY date DESC'''
        cur.execute(exeString)
        row = cur.fetchone()
        # subTime = datetime.datetime.fromisoformat(row[4])
        # shortThreshhold = datetime.datetime.now(datetime.timezone.utc) - timedelta(hours=hours)
        reString = r'\[emote:\d+:' + emotePrefix + r'[a-zA-Z]+\]'
        reStringTwo = emotePrefix + r'[a-zA-Z]+'
        reStringNumber = r'\d+'
        flag = True
        while row and flag:
            msgSentAt = datetime.datetime.fromisoformat(row[1])
            threshold = datetime.datetime.now(datetime.timezone.utc) - timedelta(days=days)
            if msgSentAt > threshold:
                emotes = re.findall(reString, row[0])
                if emotes:
                    for emote in emotes:
                        em = re.findall(reStringTwo, emote)
                        em = em[0]
                        emoteId = re.findall(reStringNumber, emote)
                        if not em in emoteList:
                            emoteList[em] = 0
                        emoteList[em] += 1
                        urls[em] = f"https://files.kick.com/emotes/{emoteId[0]}/fullsize"
            else:
                flag = False
            row = cur.fetchone()
        cur.close()
        conn.close()
        emoteList= dict(sorted(emoteList.items(), key=lambda item: item[1], reverse=True))
        emoteNames = []
        emoteUrls = []
        emoteUses = []
        for emote, num in emoteList.items():
            emoteNames.append(emote)
            emoteUrls.append(urls[emote])
            emoteUses.append(num)
        return emoteNames, emoteUrls, emoteUses
    
    def InsertKickChatToTable(self, kickId:int, kickSlug:str, content:str, identity:str, date:str, repliedto:str, channel:str):
        self.createKickChatTable()
        conn, cur = self.connectCursor()
        rowVals = (kickId, kickSlug.lower(), content, identity, date, repliedto, channel)
        exeString = '''INSERT INTO kick_chat (kick_id, kick_slug, content, identity, date, replied_to, channel) VALUES (?,?,?,?,?,?,?) '''
        cur.execute(exeString, rowVals)
        conn.commit()
        cur.close()
        conn.close()
    
    def GetKickClipByAuthor(self, kickSlug):
        clipIds = []
        self.createKickClipsTable()
        conn, cur = self.connectCursor()
        rowVals = (kickSlug,)
        exeString = '''SELECT clip_id FROM kick_clips where clip_creator_slug=? ORDER BY creation_date DESC'''
        cur.execute(exeString, rowVals)
        fetch = cur.fetchall()
        if fetch and fetch[0] != None:
            for clipId in fetch:
                clipIds.append(clipId[0])
        return clipIds
    
    def GetPlatformNames(self):
        conn, cur = self.connectCursor()
        exeString = '''SELECT platform_name FROM platforms'''
        cur.execute(exeString)
        fetch = cur.fetchall()
        platformNames = []
        for name in fetch:
            platformNames.append(name[0])
        return platformNames
    
    def GetKickClipRow(self, clipId):
        self.createKickClipsTable()
        conn, cur = self.connectCursor()
        rowVals = (clipId,)
        exeString = '''SELECT * from kick_clips WHERE clip_id=? '''
        cur.execute(exeString,rowVals)
        fetch = cur.fetchall()
        cur.close()
        conn.close()
        return fetch
        
    
    def CalculateWeeklyKickClipWinners(self):
        self.createTempClipsTable()
        self.createKickClipsHeroesTable()
        conn, cur = self.connectCursor()
        exeString = '''SELECT clip_id, livestream_id, channel_slug, clip_creator_slug, creation_date, title, views, category_slug FROM temp_kick_clips ORDER BY creation_date DESC'''
        cur.execute(exeString)
        row = cur.fetchone()
        clippersClipped = {}
        clippersViews = {}
        mostViews = 0
        mostViewsTitle = ""
        mostViewsClipper = ""
        mostViewsClipId = ""
        clipIdViews = {}
        clipdsToAdd = []
        while row:
            clipId, livestreamId, channelSlug, creatorSlug, creationDate, title, views, category = row
            oldClipRow = self.GetKickClipRow(clipId)
            if oldClipRow:
                oldclipId, oldlivestreamId, oldchannelSlug, oldcreatorSlug, oldcreationDate, oldtitle, oldviews, oldcategory = oldClipRow[0]
                clipIdViews[clipId] = views
            else:
                oldviews = 0
                clipdsToAdd.append(row)
                if not creatorSlug in clippersClipped:
                    clippersClipped[creatorSlug] = []
                clippersClipped[creatorSlug].append(clipId)
            if not creatorSlug in clippersViews:
                clippersViews[creatorSlug] = 0
            viewIncrease = views - oldviews
            clippersViews[creatorSlug] += viewIncrease
            if viewIncrease > mostViews:
                mostViews = viewIncrease
                mostViewsClipper = creatorSlug
                mostViewsTitle = title
                mostViewsClipId = clipId
            row = cur.fetchone()
        mostViewedClipper, clipperViews = self.GetMostViewedKickClipper(clippersViews)
        mostClippedClipper, numClips = self.GetMostKickClipper(clippersClipped)
        exeString = '''DROP TABLE temp_kick_clips'''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
        self.UpdateOldKickClipViews(clipIdViews)
        self.AddTempClipsToDb(clipdsToAdd)
        return mostViews, mostViewsTitle, mostViewsClipper, mostViewsClipId, mostViewedClipper, clipperViews, mostClippedClipper, numClips
    
    def AddTempClipsToDb(self, clipsToAdd:list):
        for row in clipsToAdd:
            clipId, livestreamId, channelSlug, creatorSlug, creationDate, title, views, category = row
            self.addKickClipToTable(clipId,livestreamId,channelSlug,creatorSlug,creationDate,title,views,category)

    def UpdateOldKickClipViews(self, clipIdViews:dict):
        for clipId, views in clipIdViews.items():
            self.updateKickClipViews(clipId,views)

    def GetMostViewedKickClipper(self, clipperViews:dict):
        mostViews = 0
        user = ''
        for clipperSlug, views in clipperViews.items():
            if views > mostViews:
                mostViews = views
                user = clipperSlug
        return  user, mostViews
    
    def GetMostKickClipper(self, clipperClips):
        mostClips = 0
        user = ''
        for clipperSlug, numClips in clipperClips.items():
            if len(numClips) > mostClips:
                mostClips = len(numClips)
                user = clipperSlug
        return user, mostClips

    
    def addTempKickClipToTable(self, clipId:str, livestreamId:int, channelSlug:str, clipCreatorSlug:str, creationDate:str, title:str, views:int, categorySlug:str) -> None:
        self.createTempClipsTable()
        conn, cur = self.connectCursor()
        rowVals = (clipId, livestreamId, channelSlug, clipCreatorSlug, creationDate, title, views, categorySlug)
        exeString = f'''INSERT INTO temp_kick_clips (clip_id, livestream_id, channel_slug, clip_creator_slug, creation_date, title, views, category_slug) VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(clip_id) DO NOTHING'''
        cur.execute(exeString,rowVals)
        conn.commit()
        cur.close()
        conn.close()
    
    def createTempClipsTable(self):
        conn, cur = self.connectCursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS temp_kick_clips
                (
                    clip_id TEXT PRIMARY KEY,
                    livestream_id INTEGER,
                    channel_slug TEXT,
                    clip_creator_slug TEXT,
                    creation_date TEXT,
                    title TEXT,
                    views INTEGER,
                    category_slug TEXT
                )
        ''')
        conn.commit()
        cur.close()
        conn.close()


    def GetChannelSlugFromClipId(self, clipId):
        self.createKickClipsTable()
        slug = ''
        conn, cur = self.connectCursor()
        rowVal = (clipId,)
        exeString = '''SELECT channel_slug FROM kick_clips WHERE clip_id=? '''
        cur.execute(exeString, rowVal)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            slug = fetch[0][0]
        cur.close()
        conn.close()
        return slug

    
    def GetKickClipIdTitles(self):
        self.createKickClipsTable()
        conn, cur = self.connectCursor()
        titleIdDict = {}
        exeString = '''SELECT clip_id, title FROM kick_clips '''
        cur.execute(exeString)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            for touple in fetch:
                titleIdDict[touple[1]] = touple[0]
        cur.close()
        conn.close()
        return titleIdDict
    
    def InsertClipCursor(self,cursor:str):
        self.createKickClipsTable()
        conn, cur = self.connectCursor()
        rowVal = (cursor,"greenLight")
        exeString = '''UPDATE kick_clips SET channel_slug=? WHERE clip_id=?'''
        cur.execute(exeString,rowVal)
        conn.commit()
        cur.close()
        conn.close()

    def GetClipCursor(self):
        self.createKickClipsTable()
        conn, cur = self.connectCursor()
        cursor = ''
        rowVal = ("greenLight",)
        exeString = '''SELECT channel_slug FROM kick_clips WHERE clip_id=?'''
        cur.execute(exeString,rowVal)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            cursor = fetch[0][0]
        cur.close()
        conn.close()
        return cursor
    
    def isClipRowCountZero(self):
        self.createKickClipsTable()
        conn, cur = self.connectCursor()
        exeString = '''SELECT COUNT(*) from kick_clips '''
        cur.execute(exeString)
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count == 0
    
    def isClipsFullyScanned(self):
        self.createKickClipsTable()
        conn, cur = self.connectCursor()
        isScanned = True
        rowVals = ("greenLight",)
        exeString = '''SELECT clip_id from kick_clips where clip_id=? '''
        cur.execute(exeString, rowVals)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            isScanned = False
        cur.close()
        conn.close()
        return isScanned
    
    def MarkClipsFullyScanned(self):
        self.createKickClipsTable()
        conn, cur = self.connectCursor()
        rowVals = ("greenLight",)
        exeString = '''DELETE FROM kick_clips WHERE clip_id=?'''
        cur.execute(exeString, rowVals)
        conn.commit()
        cur.close()
        conn.close()

    def GetLastSubDate(self,kickId) -> str:
        self.createKickSubTable()
        subDate = ''
        conn, cur = self.connectCursor()
        exeString = '''SELECT sub_id,user_id, date_iso from kick_subs ORDER BY sub_id DESC'''
        cur.execute(exeString)
        row = cur.fetchone()
        while row and not subDate:
            if row[1] == kickId:
                subDate = row[2]
            row = cur.fetchone()
        cur.close()
        conn.close()
        return subDate

    
    def GetKickSlugFromId(self, kickId:int) -> str:
        self.createKickUserTable()
        kickSlug = ""
        conn, cur = self.connectCursor()
        rowVals = (kickId,)
        exeString = '''SELECT slug FROM kick_users WHERE id=? '''
        cur.execute(exeString, rowVals)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            kickSlug = fetch[0][0]
        cur.close()
        conn.close()
        return kickSlug
    
    def GetKickIdFromSlug(self, kickSlug:str) -> int:
        id = 0
        self.createKickUserTable()
        conn, cur = self.connectCursor()
        rowVals = (kickSlug,)
        exeString = '''SELECT id FROM kick_users WHERE slug=? '''
        cur.execute(exeString, rowVals)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            if fetch[0][0] > 0:
                id = fetch[0][0]
        cur.close()
        conn.close()
        return id

    
    def GetKickUsersAndId(self):
        kickUsers = {}
        conn, cur = self.connectCursor()
        self.createKickUserTable()
        exeString = '''SELECT id,slug from kick_users '''
        cur.execute(exeString)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            for user in fetch:
                if user[0] > 0: #dummy kick accounts id < 0
                    kickUsers[user[1]] = user[0]
        cur.close()
        conn.close()
        return kickUsers
    
    def CreateAccountConnectionsTable(self):
        conn, cur = self.connectCursor()
        GenerateDatabase.CreateAccountConnectionsTable(cur)
        conn.commit()
        cur.close()
        conn.close()
    
    def isHasShortDate(self,kickId):
        self.createKickUserTable()
        conn, cur = self.connectCursor()
        hasDate = False
        rowVals = (kickId,)
        exeString = f'''SELECT short_role_date FROM kick_users WHERE id=?'''
        cur.execute(exeString,rowVals)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            hasDate = True
        cur.close()
        conn.close()
        return hasDate
    
    def GetShortDate(self,kickId):
        self.createKickUserTable()
        conn, cur = self.connectCursor()
        hasDate = False
        rowVals = (kickId,)
        exeString = f'''SELECT short_role_date FROM kick_users WHERE id=?'''
        cur.execute(exeString,rowVals)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            hasDate = fetch[0][0]
        cur.close()
        conn.close()
        return hasDate
    
    def GetLongDate(self,kickId):
        self.createKickUserTable()
        conn, cur = self.connectCursor()
        hasDate = False
        rowVals = (kickId,)
        exeString = f'''SELECT long_role_date FROM kick_users WHERE id=?'''
        cur.execute(exeString,rowVals)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            hasDate = fetch[0][0]
        cur.close()
        conn.close()
        return hasDate

    def isHasLongDate(self,kickId):
        self.createKickUserTable()
        conn, cur = self.connectCursor()
        hasDate = False
        rowVals = (kickId,)
        exeString = f'''SELECT long_role_date FROM kick_users WHERE id=?'''
        cur.execute(exeString,rowVals)
        fetch = cur.fetchall()
        if fetch and fetch[0][0] != None:
            hasDate = True
        cur.close()
        conn.close()
        return hasDate
    
    def InsertLongRoleDate(self,kickId, roledate = datetime.datetime.now(datetime.timezone.utc).isoformat()):
        self.createKickUserTable()
        conn, cur = self.connectCursor()
        rowVals = (roledate, kickId)
        exeString = f'''UPDATE kick_users SET long_role_date=? WHERE id=?'''
        cur.execute(exeString, rowVals)
        conn.commit()
        cur.close()
        conn.close()


    def InsertShortRoleDate(self,kickId, roledate = datetime.datetime.now(datetime.timezone.utc).isoformat()):
        self.createKickUserTable()
        conn, cur = self.connectCursor()
        rowVals = (roledate, kickId)
        exeString = f'''UPDATE kick_users SET short_role_date=? WHERE id=?'''
        cur.execute(exeString, rowVals)
        conn.commit()
        cur.close()
        conn.close()

    def GetDiscordKickConnection(self,kickId):
        self.CreateAccountConnectionsTable()
        discordId = 0
        conn, cur = self.connectCursor()
        rowVals = (kickId,)
        exeString = f'''SELECT discord_id FROM account_connections WHERE kick_id=? '''
        cur.execute(exeString,rowVals)
        fetch = cur.fetchall()
        if fetch:
            discordId = fetch[0][0]
        cur.close()
        conn.close()
        return discordId
    
    def GetKickDiscordConnection(self,discordId):
        self.CreateAccountConnectionsTable()
        kickId = 0
        conn, cur = self.connectCursor()
        rowVals = (discordId,)
        exeString = f'''SELECT kick_id FROM account_connections WHERE discord_id=? '''
        cur.execute(exeString,rowVals)
        fetch = cur.fetchall()
        if fetch:
            kickId = fetch[0][0]
        cur.close()
        conn.close()
        return kickId
    
    def GetSubTimeHours(self,hours, subTreshhold):
        self.createKickSubTable()
        conn, cur = self.connectCursor()
        exeString = '''SELECT * from kick_subs ORDER BY sub_id DESC'''
        cur.execute(exeString)
        row = cur.fetchone()
        shortSubCounts = {}
        idNameDict = {}
        while row:
            subTime = datetime.datetime.fromisoformat(row[4])
            shortThreshhold = datetime.datetime.now(datetime.timezone.utc) - timedelta(hours=hours)
            if row[1] not in idNameDict:
                idNameDict[row[1]] = row[2]
            if subTime > shortThreshhold: # larger is newer
                if row[1] not in shortSubCounts:
                    shortSubCounts[row[1]] = 0
                shortSubCounts[row[1]] += row[3]
            else:
                break
            row = cur.fetchone()
        cur.close()
        conn.close()
        shortList = {}
        for id in shortSubCounts:
            if shortSubCounts[id] >= subTreshhold:
                shortList[id] = idNameDict[id]
        return shortList
    
    def GetSubTimeDays(self,days, subThreshold):
        self.createKickSubTable()
        conn, cur = self.connectCursor()
        exeString = '''SELECT * from kick_subs ORDER BY sub_id DESC'''
        cur.execute(exeString)
        row = cur.fetchone()
        longSubCounts = {}
        idNameDict = {}
        while row:
            subTime = datetime.datetime.fromisoformat(row[4])
            longThreshhold = datetime.datetime.now(datetime.timezone.utc) - timedelta(days=days)
            if row[1] not in idNameDict:
                idNameDict[row[1]] = row[2]
            if subTime > longThreshhold: # larger is newer
                if row[1] not in longSubCounts:
                    longSubCounts[row[1]] = 0
                longSubCounts[row[1]] += row[3]
            else:
                break
            row = cur.fetchone()
        cur.close()
        conn.close()
        longList = {}
        for id in longSubCounts:
            if longSubCounts[id] >= subThreshold:
                longList[id] = idNameDict[id]
        return longList
    
    def createKickChatTable(self):
        conn, cur = self.connectCursor()
        GenerateDatabase.CreateKickChatTable(cur)
        conn.commit()
        cur.close()
        conn.close()
    
    def createDiscordUserTable(self):
        conn, cur = self.connectCursor()
        GenerateDatabase.CreateDiscordUsersTable(cur)
        conn.commit()
        cur.close()
        conn.close()
    
    def createKickUserTable(self):
        conn, cur = self.connectCursor()
        GenerateDatabase.CreateKickUsersTable(cur)
        conn.commit()
        cur.close()
        conn.close()
    
    def createKickSubTable(self):
        conn, cur = self.connectCursor()
        GenerateDatabase.CreateKickSubsTable(cur)
        conn.commit()
        cur.close()
        conn.close()

    def createConnectionsTable(self):
        conn, cur = self.connectCursor()
        GenerateDatabase.CreateAccountConnectionsTable(cur)
        conn.commit()
        cur.close()
        conn.close()
    
    def insertDiscordKickAccountConnection(self, discordId:int, kickId:int):
        self.createConnectionsTable()
        conn, cur = self.connectCursor()
        rowVals = (discordId, kickId)
        exeString = '''INSERT INTO account_connections (discord_id, kick_id) VALUES (?,?) ON CONFLICT(discord_id) DO UPDATE SET kick_id = excluded.kick_id'''
        cur.execute(exeString, rowVals)
        conn.commit()
        cur.close()
        conn.close()

    
    def insertDiscordUser(self,userId:int, userName:str):
        self.createDiscordUserTable()
        conn, cur = self.connectCursor()
        rowVals = (userId, userName)
        exeString = '''INSERT INTO discord_users (id, user_name) VALUES(?,?) ON CONFLICT(id) DO UPDATE SET user_name = excluded.user_name'''
        cur.execute(exeString, rowVals)
        conn.commit()
        cur.close()
        conn.close()
    
    def insertKickUser(self, userId:int, slug:str, channelId:int = None, chatroomId:int = None, refreshToken:str = None, email:str = None):
        self.createKickUserTable()
        conn, cur = self.connectCursor()
        slug = slug.lower()
        rowVals = (userId, slug, channelId, chatroomId, refreshToken, email)
        exeString = '''INSERT INTO kick_users (id, slug, channel_id, chatroom_id, refresh_token, email) 
                        VALUES(?,?,?,?,?,?) 
                        ON CONFLICT(id) DO UPDATE SET 
                        slug = COALESCE(excluded.slug, slug),
                        channel_id= COALESCE(excluded.channel_id, channel_id),
                        chatroom_id= COALESCE(excluded.chatroom_id, chatroom_id),
                        refresh_token= COALESCE(excluded.refresh_token, refresh_token),
                        email= COALESCE(excluded.email, email)
                    '''
        cur.execute(exeString, rowVals)
        conn.commit()
        cur.close()
        conn.close()
    
    def insertKickSub(self, gifterId:int, gifterSlug:str, numGifted:int, date:str, channel:str, selfSub = 0):
        self.createKickSubTable()
        gifterSlug = gifterSlug.lower()
        self.insertKickUser(gifterId,gifterSlug)
        conn, cur = self.connectCursor()
        rowVals = (gifterId, gifterSlug, numGifted, date, channel, selfSub)
        exeString = '''INSERT INTO kick_subs (user_id, user_slug, num_gifted, date_iso, channel, self) VALUES(?,?,?,?,?,?)'''
        cur.execute(exeString, rowVals)
        conn.commit()
        cur.close()
        conn.close()

    # Kick Clips Table Methods
    def createKickClipsHeroesTable(self):
        conn,cur = self.connectCursor()
        GenerateDatabase.CreateKickClipsHeroesTable(cur)
        conn.commit()
        cur.close()
        conn.close()

    def createKickClipsTable(self):
        conn,cur = self.connectCursor()
        GenerateDatabase.CreateKickClipsTable(cur)
        conn.commit()
        cur.close()
        conn.close()
    
    def createWeeklyKickClipsData(self,yearWeek:str, mostViewedClip:str, mostViewedClipper:str, mostClips:str):
        self.createKickClipsHeroesTable()
        conn, cur = self.connectCursor()
        rowVals = (yearWeek, mostViewedClip, mostViewedClipper, mostClips)
        exeString = '''INSERT INTO kick_clips_heroes (year_week, most_viewed_clip, most_viewed_clipper, most_clips) VALUES (?,?,?,?)'''
        cur.execute(exeString, rowVals)
        conn.commit()
        cur.close()
        conn.close()
    
    def updateKickClipViews(self, clipId:str, views:int) -> None:
        conn, cur = self.connectCursor()
        exeString = f'''UPDATE kick_clips SET views={views} WHERE clip_id='{clipId}' '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()

    def getKickClipViews(self,clipId:str, channel_slug:str) -> int:
        self.createKickClipsTable()
        views = 0
        conn, cur = self.connectCursor()
        exeString = f'''SELECT views FROM kick_clips WHERE channel_slug='{channel_slug}' AND clip_id='{clipId}' '''
        cur.execute(exeString)
        previousViews = cur.fetchall()
        if previousViews:
            views = previousViews[0][0]
        cur.close()
        conn.close()
        return views

    def addKickClipToTable(self, clipId:str, livestreamId:int, channelSlug:str, clipCreatorSlug:str, creationDate:str, title:str, views:int, categorySlug:str) -> None:
        self.createKickClipsTable()
        conn, cur = self.connectCursor()
        rowVals = (clipId, livestreamId, channelSlug, clipCreatorSlug, creationDate, title, views, categorySlug)
        exeString = f'''INSERT INTO kick_clips (clip_id, livestream_id, channel_slug, clip_creator_slug, creation_date, title, views, category_slug) VALUES (?,?,?,?,?,?,?,?)'''
        cur.execute(exeString,rowVals)
        conn.commit()
        cur.close()
        conn.close()
    
    # Confessions & Appeals Table Methods
    def createAppealsTable(self):
        conn,cur = self.connectCursor()
        GenerateDatabase.CreateAppealsTable(cur)
        conn.commit()
        cur.close()
        conn.close()

    def createConfessionsTable(self):
        conn,cur = self.connectCursor()
        GenerateDatabase.CreateConfessionsTable(cur)
        conn.commit()
        cur.close()
        conn.close()

    def addAppeal(self, appeal:str, appealTitle:str, appealerId: int, appealerName:str) -> None:
        self.createAppealsTable()
        conn,cur = self.connectCursor()
        rowVals = (appeal, appealTitle, appealerId, appealerName, time.time())
        exeString = f'''INSERT INTO appeals (appeal,appeal_title, appealer_id, appealer_name, date_added) VALUES (?,?,?,?,?)'''
        cur.execute(exeString,rowVals)
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
    
    def getUnreviewedAppeal(self):
        self.createAppealsTable()
        appealId = 0
        appeal = ""
        title = ""
        conn,cur = self.connectCursor()
        exeString = '''SELECT appeal_id, appeal,appeal_title FROM appeals WHERE date_reviewed IS NULL LIMIT 1'''
        cur.execute(exeString)
        values = cur.fetchall()
        if values:
            appealId = values[0][0]
            appeal = values[0][1]
            title = values[0][2]
        cur.close()
        conn.close()
        self.setAppealDateReviewed(appealId)
        return appealId, appeal, title
    
    def setConfessionDateReviewed(self, confessionId):
        self.createConfessionsTable()
        conn, cur = self.connectCursor()
        exeString = f'''UPDATE confessions SET date_reviewed={time.time()} WHERE confession_id={confessionId} '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def setAppealDateReviewed(self, appealId):
        self.createAppealsTable()
        conn, cur = self.connectCursor()
        exeString = f'''UPDATE appeals SET date_reviewed={time.time()} WHERE appeal_id={appealId} '''
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
    
    def reviewAppeal(self, appealId: int, approveDeny: int, reviewerId: int, reviewerName: str):
        self.createAppealsTable()
        conn, cur = self.connectCursor()
        values = (approveDeny, reviewerId, reviewerName, time.time(), appealId)
        exeString = f'''UPDATE appeals SET appeal_status=?, reviewer_id=?, reviewer_name=?, date_reviewed=? WHERE appeal_id=? '''
        cur.execute(exeString,values)
        conn.commit()
        cur.close()
        conn.close()
    
    def getUnfinishedConfessionReviews(self):
        self.createConfessionsTable()
        conn, cur = self.connectCursor()
        exeString = f'''SELECT confession_id, date_reviewed FROM confessions WHERE review_status IS NULL AND date_reviewed IS NOT NULL '''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value
    
    def getUnfinishedAppealReviews(self):
        self.createAppealsTable()
        conn, cur = self.connectCursor()
        exeString = f'''SELECT appeal_id, date_reviewed FROM appeals WHERE appeal_status IS NULL AND date_reviewed IS NOT NULL '''
        cur.execute(exeString)
        value = cur.fetchall()
        cur.close()
        conn.close()
        return value
    
    def resetAppealDateReviewed(self, appealId):
        self.createAppealsTable()
        conn, cur = self.connectCursor()
        exeString = f'''UPDATE appeals SET date_reviewed=NULL WHERE appeal_id={appealId} '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()

    def resetConfessionDateReviewed(self, confessionId):
        self.createConfessionsTable()
        conn, cur = self.connectCursor()
        exeString = f'''UPDATE confessions SET date_reviewed=NULL WHERE confession_id={confessionId} '''
        cur.execute(exeString)
        conn.commit()
        cur.close()
        conn.close()
    
    def getAllUnreviewedConfessions(self):
        self.createConfessionsTable()
        conn,cur = self.connectCursor()
        exeString = '''SELECT confession_id, confession,confession_title FROM confessions WHERE date_reviewed IS NULL'''
        cur.execute(exeString)
        values = cur.fetchall()
        cur.close()
        conn.close()
        return values
    
    def getAllUnreviewedAppeals(self):
        self.createAppealsTable()
        conn,cur = self.connectCursor()
        exeString = '''SELECT appeal_id, appeal, appeal_title FROM appeals WHERE date_reviewed IS NULL'''
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
            self.logger.error("given bad account or platform. can't update title")

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
        GenerateDatabase.CreatePlatformAccountsTable(cur)
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
            self.logger.debug("error when checking if col exists, perhaps no data yet")
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