import discord
from bot import MyClient
from credentials import load_credentials
from database import init_db, reset_isSlowed_for_all_servers


init_db()
reset_isSlowed_for_all_servers()
credentials = load_credentials('credentials.json')
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(credentials['token'])

