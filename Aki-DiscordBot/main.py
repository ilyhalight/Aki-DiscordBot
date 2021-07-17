import os

from dotenv import load_dotenv

from core.bot import bot
from scripts.console import clear

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

def do_env():
    try:
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
    except:
        print('Не удалось найти ".env" файл :c')

def run():
    bot.run(os.environ.get('DISCORD_TOKEN'))

if __name__ == '__main__':
    clear()
    do_env()
    run()



