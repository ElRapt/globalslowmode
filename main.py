
import discord
import json
from discord import app_commands
from discord.ext.commands import has_permissions
import asyncio

credentials = json.load(open('credentials.json'))

class MyClient(discord.Client):
    async def on_ready(self):
        tree.isSlowed=False;
        tree.activeSlow=False;
        tree.slowTime = 0;
        tree.embedSlow = False;
        tree.slowMessage = "Slowmode activated"
        await tree.sync(guild=discord.Object(id=credentials.get('guild_id')))
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


    async def on_message(self, message):
        if tree.activeSlow == True:
            if tree.isSlowed == False:
                tree.isSlowed=True;
                await asyncio.sleep(tree.slowTime)
                tree.isSlowed=False;
            else:
                if message.author.id == self.user.id:
                    return
                await message.author.send(tree.slowMessage)
                await message.delete()
        elif tree.embedSlow == True:
            if (message.embeds or message.attachments):
                if tree.isSlowed == False:
                    tree.isSlowed=True;
                    await asyncio.sleep(tree.slowTime)
                    tree.isSlowed=False;
                else:
                    if message.author.id == self.user.id:
                        return
                    await message.author.send(tree.slowMessage)
                    await message.delete()



        #if message.content.startswith('!ping'):
         #   await message.response.send_message(content="Only you can see this !", ephemeral=True)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name = "slowmode", description = "Launches slow mode", guild=discord.Object(id=credentials.get('guild_id'))) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@has_permissions(administrator = True)
async def first_command(interaction, seconds:int, message:str):
    try:
        tree.slowTime = int(seconds)
        tree.slowMessage = message
    except ValueError:
        await interaction.response.send_message("Enter a valid time", ephemeral=True)
        return
    await interaction.response.send_message("Slow mode activated", ephemeral=True)
    tree.activeSlow=True;

@tree.command(name = "revoke", description = "Ends true slowmode", guild=discord.Object(id=credentials.get('guild_id'))) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@has_permissions(administrator = True)
async def first_command(interaction):
    await interaction.response.send_message("Slowmode revoked", ephemeral=True)
    tree.activeSlow=False;


@tree.command(name = "embedslow", description = "Launches slow mode for embeds", guild=discord.Object(id=credentials.get('guild_id'))) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@has_permissions(administrator = True)
async def first_command(interaction, seconds:int, message:str):
    try:
        tree.slowTime = int(seconds)
        tree.slowMessage = message
    except ValueError:
        await interaction.response.send_message("Enter a valid time", ephemeral=True)
        return
    await interaction.response.send_message("Embed slow activated", ephemeral=True)
    tree.embedSlow=True;

@tree.command(name = "embedrevoke", description = "Ends true slowmode for embeds", guild=discord.Object(id=credentials.get('guild_id'))) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@has_permissions(administrator = True)
async def first_command(interaction):
    await interaction.response.send_message("Embed slowmode revoked", ephemeral=True)
    tree.embedSlow=False;


client.run(credentials.get('token'))