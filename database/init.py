import sqlite3

def reset_isSlowed_for_all_servers():
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    
    cur.execute("UPDATE Server SET isSlowed=0")
    con.commit()
    con.close()


def init_db():
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Server (
        guild_id TEXT PRIMARY KEY,
        isSlowed BOOLEAN,
        activeSlow BOOLEAN,
        slowTime INTEGER,
        embedSlow BOOLEAN,
        slowMessage TEXT
    );
    """)
    con.commit()
    con.close()

