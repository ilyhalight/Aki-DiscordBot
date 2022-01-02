import os
import sys
import discord
import aiohttp
import traceback

from core.bot import bot
from core.cogs import init_commands
from core.events import init_events
from core.logger import logger
from scripts.backup import create_backup
from scripts.checks import is_python_file
from scripts.env import get_env
from scripts.parsers.settings import settings


def run():
    try:
        init_commands()
    except:
        logger.error('Не удалось инициализировать управление когами - Пользователь: SYSTEM.')
        logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
    try:
        init_events()
    except:
        logger.error('Не удалось инициализировать ивенты - Пользователь: SYSTEM.')
        logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
    if settings['backup'] is True:
        try:
            create_backup()
        except:
            logger.error('Не удалось создать бэкап - Пользователь: SYSTEM')
            logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
    try:
        bot.run(os.environ.get('DISCORD_TOKEN'))
    except discord.LoginFailure:
        logger.critical('Этот токен недействителен')
        logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
        sys.exit(3)
    except discord.PrivilegedIntentsRequired:
        logger.critical(
            'Необходимо, чтобы были включены все привилегии.\n'
            'Перейдите на https://discord.com/developers/applications/ и включите привилегии'
        )
        logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
        sys.exit(3)
    except aiohttp.ClientConnectorError:
        logger.critical(
            'Вероятно discord.com сейчас недоступен.\n'
            'Перейдите на https://discordstatus.com/ и лично проверьте статус сервисов'
        )
        logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
        sys.exit(3)
    except AttributeError:
        logger.error(f'Не удалось найти ".env" файл - Пользователь: SYSTEM.')
        logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')


try:
    for file in os.listdir('./cogs'):
        if is_python_file(file):
            bot.load_extension(f'cogs.{file[:-3]}')
            logger.success(f'Ког "{file[:-3]}" загружен - Пользователь: SYSTEM.')
except FileNotFoundError:
    logger.error(f'Не удалось загрузить коги - Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')


if __name__ == '__main__':
    get_env()
    run()

