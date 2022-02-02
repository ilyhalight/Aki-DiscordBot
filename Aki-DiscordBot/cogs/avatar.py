import discord

from discord.ext import commands

from core.bot import avatar
from core.embeds import Errors, Helpers
from core.logger import logger
from data.colors import colors
from scripts.parsers.settings import settings


class Avatar(commands.Cog):
    """Показывает аватар пользователя"""

    def __init__(self, bot):
        self.bot = bot

    def avatar_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}аватар', value = 'Показать аватар участника', inline = False)

    async def avatar_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Аватарка')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}ава [упоминание пользователя]`\n┗ Выведет аватарку пользователя.', inline = False)
        emb.add_field(name = 'Примечание', value = f'Бот может вывести аватарку пользователей, только, текущего сервера', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Аватарка" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'avatarka', 'ava', 'avatar',
                                'аватарка', 'ава', 'аватар'
                                ])
    async def avatar_command(self, ctx, member: discord.Member = None):
        if member is None:
            user = ctx.message.author
        else:
            user = member
        emb = discord.Embed(title = f'Аватар пользователя {user}', colour = colors['black'])
        emb.set_image(url = avatar(user))
        await ctx.send(embed = emb)
        logger.info(f'Выведен аватар пользователя {user} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')


    @avatar_command.error
    async def avatar_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await Errors.custom_msg_embed(self, ctx, 'Пользователь не найден')
            logger.error(f'Не удалось вывести аватарку - Причина: Пользователь не найден — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            logger.error(error)
        else:
            await Errors.custom_msg_embed(self, ctx, error)
            logger.error(error)

def setup(bot):
    bot.add_cog(Avatar(bot))