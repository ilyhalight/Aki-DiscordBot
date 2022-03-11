import discord
from discord.ext import commands

from scripts.parsers.settings import settings
from scripts.transforms import TransformScripts
from core.discord_requests import DiscordRequest
from core.logger import logger
from core.embeds import Errors, Helpers

class UnTimeout(commands.Cog):
    """Выдача таймаута пользователю"""

    def __init__(self, bot):
        self.bot = bot

    def untimeout_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}антаймаут', value = 'Убрать таймаут пользователю', inline = False)

    async def untimeout_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Таймаут')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}антаймаут <упоминание пользователя> [причина]`\n┗ Уберёт таймаут пользователю.', inline = False)
        emb.add_field(name = 'Пример', value = f'`{settings["prefix"]}антаймаут @Toil`\n┗ Уберет таймаут пользователю Toil', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Антаймаут" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'untimeout', 'unmute',
                                'антаймаут', 'анмут', 'анмьют'
                                ])
    @commands.has_permissions(administrator = True)
    async def untimeout_command(self, ctx: commands.Context, member: discord.Member, *, reason: str = 'Не задана'):
        """Антаймаут

        Args:
            ctx (commands.Context)
            member (discord.Member): Упоминание пользователя
            reason (str, optional): Причина. По умолчнию - 'Не задана'

        Returns:
            reaction: ✅
            reaction: ❌
        """
        if member:
            if reason == 'Не задана':
                result = await DiscordRequest.user_timeout(member.id, ctx.guild.id, None)
            else:
                result = await DiscordRequest.user_timeout(member.id, ctx.guild.id, None, reason)
            if result is True:
                logger.info(f'Убран таймаут у пользователя {member.name}#{member.discriminator} (id: {member.id}) с причиной {reason} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
                return await ctx.message.add_reaction('✅')
            logger.info(f'Не удалось убрать таймаут пользователю {member.name}#{member.discriminator} (id: {member.id}) по неизвестной причине — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            return await ctx.message.add_reaction('❌')
        else:
            pass

    @untimeout_command.error
    async def untimeout_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await Errors.custom_msg_embed(self, ctx, 'Пользователь не найден')
            logger.error(f'Не удалось убрать таймаут - Причина: {error} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        elif isinstance(error, commands.errors.BadArgument):
            await self.timeout_helper(ctx)
            logger.error(f'Не удалось убрать таймаут - Причина: {error} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await Errors.custom_msg_embed(self, ctx, error)
            logger.error(f'Не удалось убрать таймаут - Причина: {error} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(UnTimeout(bot))