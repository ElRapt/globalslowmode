import discord
from bot import MyClient
from credentials import load_credentials

credentials = load_credentials('credentials.json')
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(credentials['token'])

