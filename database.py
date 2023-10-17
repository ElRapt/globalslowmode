import sqlite3
from typing import Optional, Dict


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

init_db()


def get_server_settings(guild_id: str) -> Optional[Dict]:
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Server WHERE guild_id=?", (guild_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return {
            "guild_id": row[0],
            "isSlowed": row[1],
            "activeSlow": row[2],
            "slowTime": row[3],
            "embedSlow": row[4],
            "slowMessage": row[5]
        }
    return None

def update_server_settings(guild_id: str, settings: Dict):
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO Server (
        guild_id,
        isSlowed,
        activeSlow,
        slowTime,
        embedSlow,
        slowMessage
    ) VALUES (?, ?, ?, ?, ?, ?);
    """, (
        guild_id,
        settings["isSlowed"],
        settings["activeSlow"],
        settings["slowTime"],
        settings["embedSlow"],
        settings["slowMessage"]
    ))
    con.commit()
    con.close()


def set_default_server_settings(guild_id: str):
    default_settings = {
        "guild_id": guild_id,
        "isSlowed": False,
        "activeSlow": False,
        "slowTime": 10,
        "embedSlow": False,
        "slowMessage": "Please wait before sending another message."
    }
    update_server_settings(guild_id, default_settings)
