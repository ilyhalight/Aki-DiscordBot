import discord
import traceback

from core.bot import bot
from core.logger import logger
from scripts.parsers.status import status


def init_events():
    @bot.event
    async def on_ready():
        """Устанавливаем статус боту"""
        if status['status'] in ['online', 'offline', 'idle', 'dnd', 'invisible']:
            if status['link'].startswith('www.') and status['active'] == 1 or status['link'].startswith('http') and status['active'] == 1:
                await bot.change_presence(status = status['status'], activity = discord.Activity(name = status['text'], url = status['link'], type = status['active']))
            else:
                await bot.change_presence(status = status['status'], activity = discord.Activity(name = status['text'], type = status['active']))
            logger.success('Статус бота изменен - Пользователь: SYSTEM.')

