import sqlite3
from typing import Optional, Dict


def set_slowmode_cooldown(channel_id: str, cooldown: int):
    with sqlite3.connect("settings.db") as con:
        cur = con.cursor()
        cur.execute("INSERT OR REPLACE INTO SlowModeTime (channel_id, cooldown_time) VALUES (?, ?)", (channel_id, cooldown))
        con.commit()


def remove_slowmode_cooldown(channel_id: str):
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("DELETE FROM SlowModeTime WHERE channel_id=?", (channel_id,))
    con.commit()

def get_slowmode_cooldown(channel_id: str) -> Optional[int]:
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("SELECT cooldown_time FROM SlowModeTime WHERE channel_id=?", (channel_id,))
    row = cur.fetchone()
    return row[0] if row else None