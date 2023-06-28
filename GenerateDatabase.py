import sqlite3
import time
#INTEGER = int
#REAL = float
#TEXT = string
#BLOB = bytes
#NULL = none
conn = sqlite3.connect("cassBot.db")

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS platforms
                (
                    platform_name TEXT PRIMARY KEY, 
                    last_online_message REAL,
                    last_stream_start_time REAL,
                    last_stream_end_time REAL
                )
            ''')

cur.execute('''CREATE TABLE IF NOT EXISTS subathon
                (
                    subathon INTEGER, 
                    start_time REAL,
                    end_time REAL,
                    longest_subathon INTEGER,
                    longest_subathon_time REAL
                )
            ''')

cur.execute('''CREATE TABLE IF NOT EXISTS stream
                (
                    last_online REAL, 
                    last_offline REAL,
                    last_stream_length REAL,
                    tw_img_list TEXT,
                    tw_img_queue TEXT,
                    img_pin INTEGER,
                    img_pin_url TEXT,
                    img_banned_list TEXT,
                    everyone_ping INTEGER
                )
            ''')

cur.execute('''CREATE TABLE IF NOT EXISTS user_presence_stats
                (
                    date TEXT PRIMARY KEY, 
                    weeek_day INTEGER,
                    user_presences TEXT
                )
            ''')


platform_list =[
                ("chaturbate",0,0,time.time()),
                ("onlyfans",0,0,time.time()),
                ("fansly",0,0,time.time()),
                ("twitch",0,0,time.time()),
                ("youtube",0,0,time.time()),
                ("kick",0,0,time.time()),
                ("kittiesKick",0,0,time.time())
            ]
subathon_values =[
                (0,0,0,0,None)
            ]
stream_values = [
                (0,0,0)
            ]
cur.executemany('''
                    INSERT INTO platforms (platform_name,last_online_message,last_stream_start_time,last_stream_end_time) VALUES (?,?,?,?)
                ''', platform_list)
cur.executemany('''
                    INSERT INTO subathon (subathon, start_time, end_time, longest_subathon, longest_subathon_time) VALUES (?,?,?,?,?)
                ''', subathon_values)
cur.executemany('''
                    INSERT INTO stream (last_online, last_offline, last_stream_length) VALUES (?,?,?)
                ''', stream_values)
conn.commit()

cur.close()
conn.close()