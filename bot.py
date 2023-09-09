import discord
from discord import app_commands
from settings import ServerSettings
from commands import init_bot_commands
import asyncio

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_settings = ServerSettings()
        self.tree = app_commands.CommandTree(self)
        init_bot_commands(self, self.tree)

    def get_server_settings(self, guild_id: str):
        return self.server_settings.get_server_settings(guild_id) 

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        settings = self.get_server_settings(str(message.guild.id))
        if settings['activeSlow'] == True:
            if settings['isSlowed'] == False:
                settings['isSlowed'] = True
                await asyncio.sleep(settings['slowTime'])
                settings['isSlowed'] = False
            else:
                if message.author.id == self.user.id:
                    return
                await message.author.send(settings['slowMessage'])
                await message.delete()
        elif settings['embedSlow'] == True:
            if message.embeds or message.attachments or 'https://vxtwitter.com/' in message.content:
                if settings['isSlowed'] == False:
                    settings['isSlowed'] = True
                    await asyncio.sleep(settings['slowTime'])
                    settings['isSlowed'] = False
                else:
                    if message.author.id == self.user.id:
                        return
                    await message.author.send(settings['slowMessage'])
                    await message.delete()