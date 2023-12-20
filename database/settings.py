import sqlite3
from typing import Optional

def get_channel_settings(channel_id: str):
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("SELECT channel_id, guild_id, isSlowed, activeSlow, slowTime, embedSlow, embedSlowTime, embedSlowMessage, slowMessage FROM ChannelSettings WHERE channel_id=?", (channel_id,))
    row = cur.fetchone()
    
    if row:
        return {
            'channel_id': row[0],
            'guild_id': row[1],
            'isSlowed': row[2],
            'activeSlow': row[3],
            'slowTime': row[4],
            'embedSlow': row[5],
            'embedSlowTime': row[6],  # Added embedSlowTime
            'embedSlowMessage': row[7],  # Added embedSlowMessage
            'slowMessage': row[8]
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
            'embedSlowTime': 0,  # Default value for embedSlowTime
            'embedSlowMessage': 'Default embed slow mode message',  # Default message for embedSlow
            'slowMessage': 'Default slow mode message'
        }
        set_channel_settings(channel_id, default_settings)

def set_channel_settings(channel_id: str, settings: dict):
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("REPLACE INTO ChannelSettings (channel_id, guild_id, isSlowed, activeSlow, slowTime, embedSlow, embedSlowTime, embedSlowMessage, slowMessage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (channel_id, settings['guild_id'], settings['isSlowed'], settings['activeSlow'], settings['slowTime'], settings['embedSlow'], settings['embedSlowTime'], settings['embedSlowMessage'], settings['slowMessage']))
    con.commit()
