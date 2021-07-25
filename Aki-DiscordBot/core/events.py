import discord

from core.bot import bot
from core.logger import logger
from scripts.parsers.status import status


def init_events():

    @bot.event
    async def on_ready():
        """Устанавливаем статус боту"""
        if status['status'] == 'online' or status['status'] == 'offline' or status['status'] == 'idle' or status['status'] == 'dnd' or status['status'] == 'invisible':
            if status['link'].startswith('www.') and status['active'] is 1 or status['link'].startswith('http') and status['active'] is 1:
                await bot.change_presence(status = status['status'], activity = discord.Activity(name = status['text'], url = status['link'], type = status['active']))
            else:
                await bot.change_presence(status = status['status'], activity = discord.Activity(name = status['text'], type = status['active']))
            logger.success('Статус бота изменен - Пользователь: SYSTEM')
        else:
            pass