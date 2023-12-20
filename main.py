import discord
from bot import MyBot
from utils.credentials import load_credentials
from database.init import init_db, reset_isSlowed_for_all_servers


init_db()
reset_isSlowed_for_all_servers()
credentials = load_credentials('credentials.json')
intents = discord.Intents.default()
intents.message_content = True
bot = MyBot(intents=intents)

bot.run(credentials['token'])
