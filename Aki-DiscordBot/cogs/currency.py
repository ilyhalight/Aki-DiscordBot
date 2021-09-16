import discord
import pytz

from discord.ext import commands
from datetime import datetime

from core.logger import logger
from core.bot import avatar
from scripts.parsers.currency import parse_cbr
from data.colors import colors


class Currency(commands.Cog):
    """Курс валюты (доллар, евро) за сегодня"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [
                                'currency', 'currency_course', 'currencycourse',
                                'курс', 'курс_валюты', 'курсвалюты'
                                ])
    async def currency_command(self, ctx):
        rate = parse_cbr()
        emb = discord.Embed(title = f'Курс валюты за {datetime.now(pytz.timezone("Europe/Moscow")).strftime("%d.%m.%Y")}', color = colors['help'])
        emb.add_field(name = '<:usd:887785459701415966>USD', value = f'{rate[0]} ₽', inline = True)
        emb.add_field(name = '<:euro:887784610476490805>EUR', value = f'{rate[1]} ₽', inline = True)
        emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(self.bot.user))
        emb.set_thumbnail(url = avatar(self.bot.user))
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о курсе валюты на сегодня - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Currency(bot))