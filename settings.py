from typing import Dict

class ServerSettings:
    """Handles server-specific settings."""

    def __init__(self):
        self.settings = {}  # Initialize the settings dictionary

    def get_server_settings(self, guild_id):
        if guild_id not in self.settings:
            self.settings[guild_id] = {
                'isSlowed': False,
                'activeSlow': False,
                'slowTime': 0,
                'embedSlow': False,
                'slowMessage': "Slowmode activated"
            }
        return self.settings[guild_id]
        