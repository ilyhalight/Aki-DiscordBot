from datetime import timedelta
import discord
from discord.ext import commands

from core.logger import logger
from data.colors import colors
from scripts.data_parsers.guild_verification_level import verification_level
from scripts.parsers.emojis import emojis


class GuildInfo(commands.Cog):
    """Показывает информацию о текущем сервере"""

    emoji = emojis['guild_info']

    def __init__(self, bot):
        self.bot = bot

    def guildinfo_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}сервер', value = 'Информация о сервере', inline = False)

    @commands.command(aliases = [
                                'ginfo', 'guildinfo', 'guild-info', 'guild_info', 'serverinfo', 'server-info', 'server_info', 'server', 'guild',
                                'гинфо', 'гильдияинфо', 'гильдия-инфо', 'гильдия_инфо', 'серверинфо', 'сервер-инфо', 'сервер_инфо', 'сервер', 'гильдия'
                                ])
    async def guildinfo_command(self, ctx):
        guild = ctx.message.guild
        owner = await guild.fetch_member(guild.owner_id)
        bots = 0
        guild_created = round((guild.created_at + timedelta(hours=3)).timestamp())
        emb = discord.Embed(title = f'Информация о сервере', color = colors['help'])
        emb.add_field(name = f'Название', value = guild.name, inline = True)
        emb.add_field(name = f'Уровень проверки', value = verification_level[str(guild.verification_level[0])], inline = True)
        emb.add_field(name = f'Владелец', value = f'{owner.name}#{owner.discriminator}', inline = True)
        for member in guild.members:
            if member.bot is True:
                bots += 1
        emb.add_field(name = f'Участники', value = f'{self.emoji["users"]} Всего: **{guild.member_count}**\n{self.emoji["user"]} Людей: **{guild.member_count - bots}**\n{self.emoji["bot"]} Ботов: **{bots}**', inline = True)
        all_channels = len(guild.channels) - len(guild.categories)
        if len(guild.stage_channels) != 0:
            channels_data = f'{self.emoji["all"]} Всего: **{all_channels}**\n{self.emoji["text"]} Текстовых: **{len(guild.text_channels)}**\n{self.emoji["voice"]} Голосовых: **{len(guild.voice_channels)}**\n{self.emoji["stage"]} Трибунных: **{len(guild.stage_channels)}**'
        else:
            channels_data = f'{self.emoji["all"]} Всего: **{all_channels}**\n{self.emoji["text"]} Текстовых: **{len(guild.text_channels)}**\n{self.emoji["voice"]} Голосовых: **{len(guild.voice_channels)}**'
        emb.add_field(name = f'Каналы', value = channels_data, inline = True)
        emb.add_field(name = f'Дата создания', value = f'<t:{guild_created}:D>\n<t:{guild_created}:R>', inline = True)
        emb.add_field(name = f'ID', value = guild.id, inline = True)
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
        emb.set_thumbnail(url = guild.icon_url)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о сервере {guild.name} ({guild.id}). Участники: {guild.member_count}, Боты: {bots} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(GuildInfo(bot))