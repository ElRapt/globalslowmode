import sqlite3

def reset_isSlowed_for_all_servers():
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("UPDATE ChannelSettings SET isSlowed=0")
    con.commit()
    


def init_db():
    con = sqlite3.connect("settings.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS ChannelSettings (channel_id TEXT PRIMARY KEY, guild_id TEXT, isSlowed INTEGER, activeSlow INTEGER, slowTime INTEGER, embedSlow INTEGER, embedSlowTime INTEGER, embedSlowMessage TEXT, slowMessage TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS SlowModeTime (channel_id TEXT PRIMARY KEY, cooldown_time INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Server (guild_id TEXT PRIMARY KEY, isSlowed INTEGER)")

    con.commit()
