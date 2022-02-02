import discord
import pytz

from discord.ext import commands
from datetime import datetime
from core.embeds import Helpers

from core.logger import logger
from core.bot import avatar
from scripts.parsers.currency import parse_cbr
from scripts.parsers.settings import settings
from scripts.parsers.emojis import emojis
from data.colors import colors

emoji = emojis['currency']


class Currency(commands.Cog):
    """Курс валюты (доллар, евро) на сегодня"""

    def __init__(self, bot):
        self.bot = bot

    def currency_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}курс', value = 'Курс валюты на сегодня', inline = False)

    async def cryptocurrency_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Курс валюты на сегодня')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}курс`\n┗ Выведет информацию о курсах валюты', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Курсе валюты на сегодня" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'currency', 'currency_course', 'currencycourse',
                                'курс', 'курс_валюты', 'курсвалюты'
                                ])
    async def currency_command(self, ctx):
        rate = parse_cbr()
        emb = discord.Embed(title = f'Курс валюты за {datetime.now(pytz.timezone("Europe/Moscow")).strftime("%d.%m.%Y")}', color = colors['help'])
        emb.add_field(name = f'{emoji["usd"]}USD', value = f'{rate[0]} ₽', inline = True)
        emb.add_field(name = f'{emoji["euro"]}EUR', value = f'{rate[1]} ₽', inline = True)
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(self.bot.user))
        emb.set_thumbnail(url = avatar(self.bot.user))
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о курсе валюты на сегодня — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Currency(bot))