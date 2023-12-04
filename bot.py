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
            # Skip processing if the message is from the bot itself or not from a guild
            if message.author.id == self.user.id or message.guild is None:
                return

            channel_id = str(message.channel.id)
            guild_id = str(message.guild.id)
            current_time = int(time.time())

            # Ensure channel settings exist
            ensure_channel_settings(channel_id, guild_id)

            # Fetch channel settings from the database
            settings = get_channel_settings(channel_id)
            if settings is None:
                print(f"Failed to retrieve settings for channel: {channel_id}")
                return  # Optionally, handle this scenario more gracefully

            # Get the cooldown end time for the channel from the database
            cooldown_end_time = get_slowmode_cooldown(channel_id)

            # Check if slow mode is active
            if cooldown_end_time and current_time < cooldown_end_time:
                slow_message = settings.get('slowMessage', 'You are in slow mode, please wait before sending another message.')
                await message.author.send(slow_message)
                await message.delete()
                return

            # Process the message according to the slow mode settings
            if settings.get('activeSlow') or settings.get('embedSlow'):
                # Check conditions for slow mode activation
                if settings.get('activeSlow') and not (message.embeds or message.attachments or 'https://vxtwitter.com/' in message.content):
                    # Standard message slow mode
                    self.apply_slow_mode(settings, channel_id, current_time)
                elif settings.get('embedSlow') and (message.embeds or message.attachments or 'https://vxtwitter.com/' in message.content):
                    # Embed/attachments slow mode
                    self.apply_slow_mode(settings, channel_id, current_time)

    def apply_slow_mode(self, settings, channel_id, current_time):
        # Calculate new cooldown end time and update in database
        new_cooldown_end_time = current_time + settings.get('slowTime')
        set_slowmode_cooldown(channel_id, new_cooldown_end_time)

        # Update the 'isSlowed' status in the channel settings
        settings['isSlowed'] = True
        set_channel_settings(channel_id, settings)