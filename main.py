
import discord
import json
from discord import app_commands
import asyncio

credentials = json.load(open('credentials.json'))

class MyClient(discord.Client):
    async def on_ready(self):
        tree.isSlowed=False;
        await tree.sync(guild=discord.Object(id=credentials.get('guild_id')))
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


    async def on_message(self, message):
        if tree.isSlowed == False:
            if message.author.id == self.user.id:
                return

            if message.content.startswith('!hello'):
                await message.reply('Hello!', mention_author=True)
        else:
            if message.author.id == self.user.id:
                return
            await message.reply("Slowmode on!")
            await message.delete()

        #if message.content.startswith('!ping'):
         #   await message.response.send_message(content="Only you can see this !", ephemeral=True)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "hello", description = "Says hello", guild=discord.Object(id=credentials.get('guild_id'))) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@tree.command(name = "hidden", description = "Says hello, but hidden", guild=discord.Object(id=credentials.get('guild_id'))) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    await interaction.response.send_message("Hello!", ephemeral=True)

#Command that starts a timer of 10 seconds using the library time and writes "Timer ended" when it's done.
@tree.command(name = "slowmode", description = "Starts slowmode for X seconds", guild=discord.Object(id=credentials.get('guild_id'))) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction, seconds:int):
    try:
        seconds = int(seconds)
    except ValueError:
        await interaction.response.send_message("Enter a valid time", ephemeral=True)
        return
    await interaction.response.send_message("Timer started!", ephemeral=True)
    tree.isSlowed=True;
    await asyncio.sleep(seconds)
    tree.isSlowed=False;
    await interaction.followup.send("Timer ended!", ephemeral=True)


@tree.command(name = "revoke", description = "Ends slowmode", guild=discord.Object(id=credentials.get('guild_id'))) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    await interaction.response.send_message("Slowmode revoked", ephemeral=True)
    tree.isSlowed=False;

client.run(credentials.get('token'))