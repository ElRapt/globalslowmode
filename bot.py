import discord
from database.settings import get_server_settings, update_server_settings, set_default_server_settings
import asyncio

cogs_list = [
    'slow',
    'embedslow',
]


class MyBot(discord.bot.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for cog in cogs_list:
            self.load_extension(f'cogs.{cog}')

    def get_server_settings(self, guild_id: str):
        settings = get_server_settings(guild_id)
        if not settings:
            set_default_server_settings(guild_id)
            settings = get_server_settings(guild_id)
        return settings


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        settings = self.get_server_settings(str(message.guild.id))
        print(settings)
        
        if settings.get('activeSlow') == 1:  # True is represented as 1
            if settings.get('isSlowed') == 0:  # False is represented as 0
                settings['isSlowed'] = 1  # True
                update_server_settings(str(message.guild.id), settings)
                await asyncio.sleep(settings.get('slowTime'))
                settings['isSlowed'] = 0  # False
                update_server_settings(str(message.guild.id), settings)
            else:
                if message.author.id == self.user.id:
                    return
                await message.author.send(settings.get('slowMessage', ''))
                await message.delete()

        elif settings.get('embedSlow') == 1:  # True is represented as 1
            if message.embeds or message.attachments or 'https://vxtwitter.com/' in message.content:
                if settings.get('isSlowed') == 0:  # False is represented as 0
                    settings['isSlowed'] = 1  # True
                    update_server_settings(str(message.guild.id), settings)
                    await asyncio.sleep(settings.get('slowTime'))
                    settings['isSlowed'] = 0  # False
                    update_server_settings(str(message.guild.id), settings)
                else:
                    if message.author.id == self.user.id:
                        return
                    await message.author.send(settings.get('slowMessage', ''))
                    await message.delete()
