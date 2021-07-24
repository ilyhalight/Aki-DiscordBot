import discord

from discord.ext import commands

from core.bot import avatar
from scripts.parsers.owner import owner
from scripts.parsers.settings import settings
from core.logger import logger
from data.colors import colors
from data.info import __version__, __status__

class Bot_info(commands.Cog):
    """Show bot info"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [
                                'info', 'bot', 'bot_info', 'botinfo', 'information',
                                'инфо', 'бот', 'бот_инфо', 'ботинфо', 'информация'
                                ])
    async def botinfo_command (self, ctx):
        emb = discord.Embed(title = ctx.guild.name, description = f'Информация о боте **{self.bot.user.name}**.\nПодробнее о командах - `{settings["prefix"]}хелп`', color = colors['help'])
        emb.add_field(name = f'<:creator:868465769707601920>Создатель:', value = f'⠀⠀{owner["name"]}#{owner["tag"]}', inline = True)
        emb.add_field(name = f'<:license:868473632035340349>Лицензия:', value = '⠀⠀MIT License', inline = True)
        emb.add_field(name = f'<:status:868474272950128650>Статус:', value = f'⠀⠀{__status__}', inline = True)
        emb.add_field(name = f'<:version:868474836568145940>Версия:', value = f'⠀⠀{__version__}', inline = True)
        emb.add_field(name = f'<:github:868478604365922314>GitHub:', value = f'⠀⠀[Тык](https://github.com/ilyhalight)', inline = True)
        emb.set_thumbnail(url = avatar(self.bot.user))
        emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(self.bot.user))
        await ctx.send(embed = emb)
        logger.info(f'Информация о Боте - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Bot_info(bot))