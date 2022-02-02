import discord
import random
from discord.ext import commands

from core.embeds import Errors, Helpers
from core.logger import logger
from scripts.parsers.settings import settings


class Random(commands.Cog):
    """Показать рандомное число"""

    def __init__(self, bot):
        self.bot = bot

    def random_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}рандом', value = 'Получить рандомное число', inline = False)

    async def random_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Рандом')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}рандом <число 1> [число 2]`\n┗ Вернёт рандомное число', inline = False)
        emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}рандом 5`\n┗ Вернёт рандомное число от 1 до 5.', inline = False)
        emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}рандом 5 10`\n┗ Вернёт рандомное число от 5 до 10.', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "рандом" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = ['random', 'rand', 'рандом', 'ранд'])
    async def random_command(self, ctx, count: int = None, count1: int = None):
        if count == None and count1 == None:
            await self.random_helper(ctx)
        if count != None and count1 == None:
            await ctx.send(str(random.randint(int(1), int(count))))
            logger.info(f'Рандомное число от 1 до {count} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        if count != None and count1 != None:
            await ctx.send(str(random.randint(int(count), int(count1))))
            logger.info(f'Рандомное число от {count} до {count1} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')


    @random_command.error
    async def random_command_error(self, ctx, error):
        if isinstance (error, commands.BadArgument):
            await Errors.custom_msg_embed(self, ctx, f'Использованы буквы в {settings["prefix"]}рандом')
            logger.error(f'Не удалось использовать команду random - Причина: Использованы буквы — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            logger.error(error)

def setup(bot):
    bot.add_cog(Random(bot))