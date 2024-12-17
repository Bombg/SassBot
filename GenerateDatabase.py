import sqlite3
import time
#INTEGER = int
#REAL = float
#TEXT = string
#BLOB = bytes
#NULL = none
conn = sqlite3.connect("sassBot.db")

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS platforms
                (
                    platform_name TEXT PRIMARY KEY, 
                    last_online_message REAL,
                    last_stream_start_time REAL,
                    last_stream_end_time REAL,
                    rerun_playing INTEGER
                )
            ''')

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
                    everyone_ping INTEGER,
                    rerun_ping INTEGER
                )
            ''')

cur.execute('''CREATE TABLE IF NOT EXISTS user_presence_stats
                (
                    date TEXT PRIMARY KEY, 
                    week_day INTEGER,
                    user_presences TEXT
                )
            ''')

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

cur.execute('''CREATE TABLE IF NOT EXISTS appeals
                (
                    appeal_id INTEGER PRIMARY KEY,
                    appeal TEXT,
                    appeal_title TEXT,
                    appeal_status INTEGER,
                    appealer_id INTEGER,
                    appealer_name TEXT,
                    reviewer_id INTEGER,
                    reviewer_name TEXT,
                    date_added INTEGER,
                    date_reviewed INTEGER
                )
            ''')

platform_list =[
                ("chaturbate",0,0,0),
                ("onlyfans",0,0,0),
                ("fansly",0,0,0),
                ("twitch",0,0,0),
                ("youtube",0,0,0),
                ("kick",0,0,0),
                ("cam4",0,0,0),
                ("mfc",0,0,0),
                ("bongacams",0,0,0),
                ("stripchat",0,0,0),
                ("eplay",0,0,0),
                ("manyvids",0,0,0)
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