import discord
import time
import logging
from database.settings import get_channel_settings, set_channel_settings, ensure_channel_settings
from database.slowmode import get_slowmode_cooldown, set_slowmode_cooldown

cogs_list = [
    'slow',
    'embedslow',
    'help'
]

logging.basicConfig(level=logging.INFO)

class MyBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_cogs()

    def load_cogs(self):
        for cog in cogs_list:
            try:
                self.load_extension(f'cogs.{cog}')
            except Exception as e:
                logging.error(f"Error loading cog {cog}: {e}")

    async def on_ready(self):
        logging.info(f'Logged in as {self.user} (ID: {self.user.id})')



    async def on_message(self, message):
        
        if self.is_message_ignorable(message):
            return

        try:
            await self.handle_message(message)
        except discord.errors.Forbidden as e:
            logging.warning(f"Permission error: {e}")
        except discord.errors.HTTPException as e:
            logging.warning(f"Discord HTTP error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    def is_message_ignorable(self, message):
        return message.author.id == self.user.id or message.guild is None

    async def handle_message(self, message):
        channel_id = str(message.channel.id)
        settings = self.fetch_channel_settings(channel_id)
        if settings:
            logging.info(f"Checking message in channel {channel_id} from {message.author.display_name}")
            if settings.get('activeSlow') or settings.get('embedSlow'):
                await self.check_and_apply_slow_mode(message, settings, channel_id)


    def fetch_channel_settings(self, channel_id):
        settings = get_channel_settings(channel_id)
        if settings is None:
            logging.warning(f"Failed to retrieve settings for channel: {channel_id}")
        return settings

    async def check_and_apply_slow_mode(self, message, settings, channel_id):
        ensure_channel_settings(channel_id, str(message.guild.id))
        current_time = int(time.time())
        cooldown_end_time = get_slowmode_cooldown(channel_id)

        
        has_embeds_or_attachments = bool(message.embeds) or bool(message.attachments)
        contains_special_link = 'https://vxtwitter.com/' in message.content or 'https://fxtwitter.com/' in message.content
        contains_discord_cdn_link = any([
            'https://cdn.discordapp' in message.content,
            'https://media.discordapp' in message.content,
            'https://images-ext-1.discordapp' in message.content,
            'https://images-ext-2.discordapp' in message.content
        ])

        is_special_message = has_embeds_or_attachments or contains_special_link or contains_discord_cdn_link

        
        slow_mode_active = False
        slow_time = 0
        slow_message = ''

        
        if is_special_message and settings.get('embedSlow'):
            slow_mode_active = cooldown_end_time and current_time < cooldown_end_time
            slow_time = settings.get('embedSlowTime', 60)
            slow_message = settings.get('embedSlowMessage', 'Please wait before sending another special message.')

        
        elif not is_special_message and settings.get('activeSlow'):
            slow_mode_active = cooldown_end_time and current_time < cooldown_end_time
            slow_time = settings.get('slowTime', 60)
            slow_message = settings.get('slowMessage', 'Please wait before sending another message.')

        if slow_mode_active:
            await message.delete()
            await message.author.send(slow_message)
        elif slow_time > 0:
            self.apply_slow_mode(slow_time, channel_id, current_time)



    def apply_slow_mode(self, slow_time, channel_id, current_time):
        new_cooldown_end_time = current_time + slow_time
        set_slowmode_cooldown(channel_id, new_cooldown_end_time)
