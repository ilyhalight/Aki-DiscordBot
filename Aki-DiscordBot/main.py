import os
import discord

from dotenv import load_dotenv

from core.bot import bot


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

def do_env():
    try:
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
    except:
        print('Не удалось найти файл ".env".')

def run():
    bot.run(os.environ.get('DISCORD_TOKEN'))

if __name__ == '__main__':
    do_env()
    run()



