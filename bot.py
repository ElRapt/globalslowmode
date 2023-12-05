import discord
import time
from database.settings import get_channel_settings, set_channel_settings, ensure_channel_settings
from database.slowmode import get_slowmode_cooldown, set_slowmode_cooldown


cogs_list = [
    'slow',
    'embedslow',
    'help'
]


class MyBot(discord.bot.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for cog in cogs_list:
            self.load_extension(f'cogs.{cog}')

    def get_channel_settings(self, guild_id: str):
        settings = get_channel_settings(guild_id)
        if not settings:
            ensure_channel_settings(guild_id)
            settings = get_channel_settings(guild_id)
        return settings


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
            
    async def on_message(self, message):
            if message.author.id == self.user.id or message.guild is None:
                return

            channel_id = str(message.channel.id)
            guild_id = str(message.guild.id)
            current_time = int(time.time())

            ensure_channel_settings(channel_id, guild_id)

            settings = get_channel_settings(channel_id)
            if settings is None:
                print(f"Failed to retrieve settings for channel: {channel_id}")
                return  

            cooldown_end_time = get_slowmode_cooldown(channel_id)

            if cooldown_end_time and current_time < cooldown_end_time:
                slow_message = settings.get('slowMessage', 'You are in slow mode, please wait before sending another message.')
                await message.author.send(slow_message)
                await message.delete()
                return

            if settings.get('activeSlow') or settings.get('embedSlow'):
                if settings.get('activeSlow') and not (message.embeds or message.attachments or 'https://vxtwitter.com/' in message.content):
                    self.apply_slow_mode(settings, channel_id, current_time)
                    
                elif settings.get('embedSlow') and (message.embeds or message.attachments or 'https://vxtwitter.com/' in message.content):
                    self.apply_slow_mode(settings, channel_id, current_time)

    def apply_slow_mode(self, settings, channel_id, current_time):
        new_cooldown_end_time = current_time + settings.get('slowTime')
        set_slowmode_cooldown(channel_id, new_cooldown_end_time)

        settings['isSlowed'] = True
        set_channel_settings(channel_id, settings)