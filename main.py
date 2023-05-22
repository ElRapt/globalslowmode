import discord
import json
from discord import app_commands
from discord.ext.commands import has_permissions
import asyncio

credentials = json.load(open('credentials.json'))

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_settings = {}  # Initialize the settings dictionary

    def get_server_settings(self, guild_id):
        if guild_id not in self.server_settings:
            self.server_settings[guild_id] = {
                'isSlowed': False,
                'activeSlow': False,
                'slowTime': 0,
                'embedSlow': False,
                'slowMessage': "Slowmode activated"
            }
        return self.server_settings[guild_id]

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        settings = self.get_server_settings(message.guild.id)
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

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "slowmode", description = "Launches slow mode") 
@has_permissions(administrator = True)
async def first_command(interaction, seconds:int, message:str):
    settings = client.get_server_settings(interaction.guild.id)
    try:
        settings['slowTime'] = int(seconds)
        settings['slowMessage'] = message
    except ValueError:
        await interaction.response.send_message("Enter a valid time", ephemeral=True)
        return
    await interaction.response.send_message("Slow mode activated", ephemeral=True)
    settings['activeSlow'] = True

@tree.command(name = "revoke", description = "Ends true slowmode") 
@has_permissions(administrator = True)
async def first_command(interaction):
    settings = client.get_server_settings(interaction.guild.id)
    settings['activeSlow'] = False
    await interaction.response.send_message("Slowmode revoked", ephemeral=True)

@tree.command(name = "embedslow", description = "Launches slow mode for embeds")
@has_permissions(administrator = True)
async def first_command(interaction, seconds:int, message:str):
    settings = client.get_server_settings(interaction.guild.id)
    try:
        settings['slowTime'] = int(seconds)
        settings['slowMessage'] = message
    except ValueError:
        await interaction.response.send_message("Enter a valid time", ephemeral=True)
        return
    await interaction.response.send_message("Embed slow activated", ephemeral=True)
    settings['embedSlow'] = True

@tree.command(name = "embedrevoke", description = "Ends true slowmode for embeds")
@has_permissions(administrator = True)
async def first_command(interaction):
    settings = client.get_server_settings(interaction.guild.id)
    settings['embedSlow'] = False
    await interaction.response.send_message("Embed slowmode revoked", ephemeral=True)

client.run(credentials.get('token'))

