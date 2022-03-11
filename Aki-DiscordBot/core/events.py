import discord

from core.bot import bot
from core.logger import logger
from core.discord_requests import DiscordRequest
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

    @bot.event
    async def on_message(msg):
        await bot.process_commands(msg)
        if msg.author is not bot.user:
            msg_array = msg.content.split(' ')
            if not msg_array[0].startswith('$'):
                warn_message = 0
                author_id = msg.author.id
                guild_id = msg.guild.id
                if msg.author.bot is False:
                    for message in msg_array:
                        if message == '[DU]':
                            break
                        elif message.lower() in ['@everyone', '@here']:
                            logger.warning(message)
                            warn_message += 3
                            break
                        elif message.lower() in ['дискорд', 'раздаёт', 'раздача', 'актив', 'халява', 'зайдите', 'залетите', 'стрим'] or message.lower().startswith('https://discord.gg/'):
                            logger.warning(message)
                            warn_message += 1
                        else:
                            pass
                    if warn_message >= 3:
                        result = await DiscordRequest.user_timeout(author_id, guild_id, 10080, "Подозрение в рекламе")
                        if result:
                            logger.info(f'Пользователю {msg.author.name}#{msg.author.discriminator} (id: {author_id}) был выдан таймаут за подозрение в рекламе — Автоматическое срабатывание')

