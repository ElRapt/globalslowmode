
import sqlite3
from typing import Optional



def get_channel_settings(channel_id: str):
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("SELECT channel_id, guild_id, isSlowed, activeSlow, slowTime, embedSlow, slowMessage FROM ChannelSettings WHERE channel_id=?", (channel_id,))
    row = cur.fetchone()
    con.close()
    
    if row:
        return {
            'channel_id': row[0],
            'guild_id': row[1],
            'isSlowed': row[2],
            'activeSlow': row[3],
            'slowTime': row[4],
            'embedSlow': row[5],
            'slowMessage': row[6]
        }
    else:
        return None
    
    
def ensure_channel_settings(channel_id: str, guild_id: str):
    settings = get_channel_settings(channel_id)
    if settings is None:
        default_settings = {
            'channel_id': channel_id,
            'guild_id': guild_id,
            'isSlowed': False,
            'activeSlow': False,
            'slowTime': 0,
            'embedSlow': False,
            'slowMessage': 'Default slow mode message'
        }
        set_channel_settings(channel_id, default_settings)
        
def set_channel_settings(channel_id: str, settings: dict):
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("REPLACE INTO ChannelSettings (channel_id, guild_id, isSlowed, activeSlow, slowTime, embedSlow, slowMessage) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (channel_id, settings['guild_id'], settings['isSlowed'], settings['activeSlow'], settings['slowTime'], settings['embedSlow'], settings['slowMessage']))
    con.commit()
    con.close()
