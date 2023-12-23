import discord
import asyncio
from bot import MyBot
from utils.credentials import load_credentials
from database.init import init_db, reset_isSlowed_for_all_servers


init_db()
reset_isSlowed_for_all_servers()
credentials = load_credentials('credentials.json')
intents = discord.Intents.default()
intents.message_content = True
bot = MyBot(intents=intents)

async def reconnect_loop():
    while True:
        await asyncio.sleep(1)
        if bot.is_closed():
            print('Bot is disconnected, attempting to reconnect...')
            try:
                await bot.start(credentials['token'])
                print('Reconnect successful.')
                break
            except Exception as e:
                print(f'Reconnect failed, {e}, retrying in 5 seconds...')
                await asyncio.sleep(5)

async def main():
    try:
        await bot.start(credentials['token'])
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal exception {e}, running reconnect loop.")
        await reconnect_loop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
