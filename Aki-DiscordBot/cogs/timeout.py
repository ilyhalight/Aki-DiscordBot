import discord
from discord.ext import commands

from scripts.parsers.settings import settings
from scripts.transforms import TransformScripts
from core.discord_requests import DiscordRequest
from core.logger import logger
from core.embeds import Errors, Helpers

class Timeout(commands.Cog):
    """Выдача таймаута пользователю"""

    def __init__(self, bot):
        self.bot = bot

    def timeout_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}таймаут', value = 'Выдать таймаут пользователю', inline = False)

    async def timeout_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Таймаут')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}таймаут <упоминание пользователя> <время> [причина]`\n┗ Выдаст таймаут пользователю.', inline = False)
        emb.add_field(name = 'Пример', value = f'`{settings["prefix"]}таймаут @Toil 7d`\n┗ Выдаст таймаут пользователю Toil на 7 дней', inline = False)
        emb.add_field(name = 'Примечание', value = f'Время таймаута не может бысть указано в секундах/месяцах/годах', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Таймаут" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'timeout', 'mute',
                                'таймаут', 'мут', 'мьют'
                                ])
    @commands.has_permissions(administrator = True)
    async def timeout_command(self, ctx: commands.Context, member: discord.Member, until: str, *, reason: str = 'Не задана'):
        """Выдача таймаута на время

        Args:
            ctx (commands.Context)
            member (discord.Member): Упоминание пользователя
            until (str): Срок действия. Не может быть больше 28 дней
            reason (str, optional): Причина наказания. По умолчнию - 'Не задана'

        Returns:
            reaction: ✅
            reaction: ❌
        """
        if all((member, until)) and until[0] in [str(i) for i in range(1, 10)]:
            minutes = TransformScripts.transform_to_minute(until)
            if minutes > 2419200:
                minutes = 2419200
            if reason == 'Не задана':
                result = await DiscordRequest.user_timeout(member.id, ctx.guild.id, minutes)
            else:
                result = await DiscordRequest.user_timeout(member.id, ctx.guild.id, minutes, reason)
            if result is True:
                logger.info(f'Выдан таймаут пользователю {member.name}#{member.discriminator} (id: {member.id}) на срок "{until}" с причиной {reason} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
                return await ctx.message.add_reaction('✅')
            logger.info(f'Не удалось выдать таймаут пользователю {member.name}#{member.discriminator} (id: {member.id}) по неизвестной причине — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            return await ctx.message.add_reaction('❌')
        else:
            pass

    @timeout_command.error
    async def timeout_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await Errors.custom_msg_embed(self, ctx, 'Пользователь не найден')
            logger.error(f'Не удалось выдать таймаут - Причина: {error} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        elif isinstance(error, commands.errors.BadArgument):
            await self.timeout_helper(ctx)
            logger.error(f'Не удалось выдать таймаут - Причина: {error} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await Errors.custom_msg_embed(self, ctx, error)
            logger.error(f'Не удалось выдать таймаут - Причина: {error} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Timeout(bot))