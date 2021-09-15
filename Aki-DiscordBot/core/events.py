import discord
import traceback

from core.bot import bot
from core.logger import logger
try:
    from scripts.parsers.status import status
except ImportError:
    logger.error('Не удалось загрузить модуль scripts/parsers/status.py - Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')


def init_events():
    @bot.event
    async def on_ready():
        """Устанавливаем статус боту"""
        try:
            if status['status'] in ['online', 'offline', 'idle', 'dnd', 'invisible']:
                if status['link'].startswith('www.') and status['active'] == 1 or status['link'].startswith('http') and status['active'] == 1:
                    await bot.change_presence(status = status['status'], activity = discord.Activity(name = status['text'], url = status['link'], type = status['active']))
                else:
                    await bot.change_presence(status = status['status'], activity = discord.Activity(name = status['text'], type = status['active']))
                logger.success('Статус бота изменен - Пользователь: SYSTEM.')
        except NameError:
            logger.error('Не удалось установить статус бота - Пользователь: SYSTEM.')
            logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

