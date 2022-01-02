from inspect import Arguments
import traceback
import discord
import random
from discord.ext import commands

from core.bot import avatar, bot
from core.logger import logger
from data.colors import colors
from scripts.parsers.settings import settings
try:
    from scripts.parsers.imgs import imgs
except ImportError:
    logger.error('Не удалось загрузить модуль scripts/parsers/imgs.py - Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')



class Random(commands.Cog):
    """Show random number"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['random', 'rand', 'рандом', 'ранд'])
    async def random_command(self, ctx, count: int = None, count1: int = None):
        if count == None and count1 == None:
            emb = discord.Embed(title = 'Помощник - Рандом', color = colors['help'])
            emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}рандом <число 1> [число 2]`', inline = False)
            emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}рандом 5`\n┗ Вернёт рандомное число от 1 до 5.', inline = False)
            emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}рандом 5 10`\n┗ Вернёт рандомное число от 5 до 10.', inline = False)
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(self.bot.user))
            emb.set_thumbnail(url = avatar(self.bot.user))
            await ctx.send(embed = emb)
            logger.info(f'Информация о "рандом" - Пользователь: {ctx.author} ({ctx.author.id}).')
        if count != None and count1 == None:
            await ctx.send(str(random.randint(int(1), int(count))))
            logger.info(f'Рандомное число от 1 до {count} - Пользователь: {ctx.author} ({ctx.author.id}).')
        if count != None and count1 != None:
            await ctx.send(str(random.randint(int(count), int(count1))))
            logger.info(f'Рандомное число от {count} до {count1} - Пользователь: {ctx.author} ({ctx.author.id}).')

    @random_command.error
    async def random_command_error(self, ctx, error):
        if isinstance (error, commands.BadArgument):
            emb = discord.Embed(description = f'Использованы буквы в {settings["prefix"]}рандом\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['error']) # Не будет работать, если нету json с картинками
            await ctx.send(embed = emb)
            logger.error(f'Не удалось использовать команду random  - Причина: Использованы буквы - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Random(bot))