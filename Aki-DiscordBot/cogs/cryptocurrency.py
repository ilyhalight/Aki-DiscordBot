import discord
import pytz

from discord.ext import commands
from datetime import datetime

from core.logger import logger
from core.bot import avatar
from scripts.parsers.cryptocurrency import parse_cryptonator
from data.colors import colors


class CryptoCurrency(commands.Cog):
    """Курс криптовалюты (btc, eth и т.д) за сегодня"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [
                                'cryptocurrency', 'crypto_currency',
                                'криптокурс', 'курс_крипты', 'курскрипты', 'курс_криптовалюты', 'курскриптовалюты'
                                ])
    async def cryptocurrency_command(self, ctx):
        emb = discord.Embed(title = f'Курс крипты за {datetime.now(pytz.timezone("Europe/Moscow")).strftime("%d.%m.%Y")}', color = colors['help'])
        parse_cryptonator(emb)
        emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(self.bot.user))
        emb.set_thumbnail(url = avatar(self.bot.user))
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о курсе криптовалюты на сегодня - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(CryptoCurrency(bot))