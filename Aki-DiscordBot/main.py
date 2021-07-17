import os
from core.cogs import init_commands

from dotenv import load_dotenv

from core.bot import bot
from scripts.checks import is_python_file
from scripts.console import clear

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

def do_env():
    try:
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
    except:
        print('Не удалось найти ".env" файл :c')

def run():
    try:
        init_commands()
    except:
        print('Не удалось инициализировать основые комманды')
    bot.run(os.environ.get('DISCORD_TOKEN'))

for file in os.listdir('./cogs'):
    if is_python_file(file):
        bot.load_extension(f'cogs.{file[:-3]}') # Загрузка когов.

if __name__ == '__main__':
    clear()
    do_env()
    run()



