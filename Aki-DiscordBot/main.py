import os
import sys
import discord
import aiohttp
from dotenv import load_dotenv

from core.bot import bot
from core.cogs import init_commands
from core.logger import logger
from scripts.checks import is_python_file
from scripts.console import clear



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

def do_env():
    try:
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
    except:
        logger.critical('Не удалось найти ".env" файл - Пользователь: SYSTEM.')
        sys.exit(3)

def run():
    try:
        init_commands()
    except:
        logger.error('Не удалось инициализировать управление когами - Пользователь: SYSTEM.')
    try:
        bot.run(os.environ.get('DISCORD_TOKEN'))
    except discord.LoginFailure:
        logger.critical('Этот токен недействителен')
        sys.exit(3)
    except discord.PrivilegedIntentsRequired:
        logger.critical('Необходимо, чтобы были включены все привилегии.\n'
                        'Перейдите на https://discord.com/developers/applications/ и включите привилегии')
        sys.exit(3)
    except aiohttp.ClientConnectorError:
        logger.critical(
            'Вероятно discord.com сейчас недоступен.\n'
            'Перейдите на https://discordstatus.com/ и лично проверьте статус сервисов'
        )
        sys.exit(3)

clear()
for file in os.listdir('./cogs'):
    if is_python_file(file):
        bot.load_extension(f'cogs.{file[:-3]}')
        logger.success(f'Ког "{file[:-3]}" загружен - Пользователь: SYSTEM.')


if __name__ == '__main__':
    do_env()
    run()



