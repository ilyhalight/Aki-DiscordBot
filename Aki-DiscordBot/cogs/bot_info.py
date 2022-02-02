import discord
from discord.ext import commands

from core.bot import avatar
from core.embeds import Errors, Helpers
from core.logger import logger
from scripts.parsers.owner import owner
from scripts.parsers.settings import settings
from scripts.parsers.emojis import emojis
from scripts.parsers.info import info
from data.colors import colors

emoji = emojis['bot_info']


class BotInfo(commands.Cog):
    """Показывает информацию о боте"""

    def __init__(self, bot):
        self.bot = bot

    def botinfo_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}бот', value = 'Информация о боте', inline = False)

    async def botinfo_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Информация о боте')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}бот`\n┗ Выведет информацию о боте.', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Информация о боте" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'info', 'bot', 'bot_info', 'botinfo', 'information',
                                'инфо', 'бот', 'бот_инфо', 'ботинфо', 'информация'
                                ])
    async def botinfo_command (self, ctx):
        emb = discord.Embed(title = ctx.guild.name, description = f'Информация о боте **{self.bot.user.name}**.\nПодробнее о командах - `{settings["prefix"]}хелп`', color = colors['help'])
        emb.add_field(name = f'{emoji["creator"]}Создатель:', value = f'⠀⠀{owner["name"]}#{owner["tag"]}', inline = True)
        emb.add_field(name = f'{emoji["license"]}Лицензия:', value = '⠀⠀MIT License', inline = True)
        emb.add_field(name = f'{emoji["status"]}Статус:', value = f'⠀⠀{info["status"]}', inline = True)
        emb.add_field(name = f'{emoji["version"]}Версия:', value = f'⠀⠀{info["version"]}', inline = True)
        emb.add_field(name = f'{emoji["github"]}GitHub:', value = f'⠀⠀[Тык](https://github.com/ilyhalight/Aki-DiscordBot)', inline = True)
        emb.set_thumbnail(url = avatar(self.bot.user))
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(self.bot.user))
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о Боте — Запросил пользователь: {ctx.author} ({ctx.author.id}).')


    @botinfo_command.error
    async def botinfo_command_error(self, ctx, error):
        await Errors.custom_msg_embed(self, ctx, error)
        logger.error(error)

def setup(bot):
    bot.add_cog(BotInfo(bot))