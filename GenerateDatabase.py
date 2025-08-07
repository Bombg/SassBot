import sqlite3

#INTEGER = int
#REAL = float
#TEXT = string
#BLOB = bytes
#NULL = none

def CreateKickChatTable(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS kick_chat
                (
                    id INTEGER PRIMARY KEY,
                    kick_id INTEGER,
                    kick_slug TEXT,
                    content TEXT,
                    identity TEXT,
                    date TEXT,
                    replied_to TEXT,
                    channel TEXT,
                    FOREIGN KEY (kick_id) REFERENCES kick_users(id)
                )
    ''')

def CreateKickUsersTable(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS kick_users
            (
                id INTEGER PRIMARY KEY,
                slug TEXT,
                channel_id INTEGER,
                chatroom_id INTEGER,
                email TEXT,
                refresh_token TEXT,
                long_role_date TEXT,
                short_role_date TEXT
            )
    ''')

def CreateKickSubsTable(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS kick_subs
            (
                sub_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                user_slug TEXT,
                num_gifted INTEGER,
                date_iso TEXT,
                self INTEGER,
                channel TEXT,
                FOREIGN KEY(user_id) REFERENCES kick_users(id)
            )
    ''')

def CreateDiscordUsersTable(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS discord_users
            (
                id INTEGER PRIMARY KEY,
                user_name TEXT
            )
    ''')

def CreateAccountConnectionsTable(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS account_connections
            (
                discord_id INTEGER PRIMARY KEY,
                kick_id TEXT,
                FOREIGN KEY(discord_id) REFERENCES discord_users(id),
                FOREIGN KEY(kick_id) REFERENCES kick_users(id)
            )
    ''')

def CreateKickClipsHeroesTable(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS kick_clips_heroes
            (
                year_week TEXT PRIMARY KEY,
                most_viewed_clip TEXT,
                most_viewed_clipper TEXT,
                most_clips TEXT,
                FOREIGN KEY(most_viewed_clip) REFERENCES kick_clips(clip_id)
            )
    ''')

def CreateKickClipsTable(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS kick_clips
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

def CreateAppealsTable(cur):
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

def CreateConfessionsTable(cur):
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
    
def CreatePlatformAccountsTable(cur):
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

def GenerateDatabase():
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

    CreatePlatformAccountsTable(cur)

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

    CreateConfessionsTable(cur)
    CreateAppealsTable(cur)
    CreateKickClipsTable(cur)
    CreateKickClipsHeroesTable(cur)
    CreateKickUsersTable(cur)
    CreateDiscordUsersTable(cur)
    CreateAccountConnectionsTable(cur)
    CreateKickSubsTable(cur)

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

if __name__ == "__main__":
    GenerateDatabase()