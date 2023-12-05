-- Drop the existing table
DROP TABLE IF EXISTS SlowModeTime;

-- Recreate the table without guild_id
CREATE TABLE SlowModeTime (
    channel_id TEXT PRIMARY KEY,
    cooldown_time INTEGER NOT NULL
);
