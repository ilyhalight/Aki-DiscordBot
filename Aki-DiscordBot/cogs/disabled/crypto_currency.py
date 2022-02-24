import discord
import pytz

from discord.ext import commands
from datetime import datetime
from core.embeds import Helpers

from core.logger import logger
from core.bot import avatar
from scripts.parsers.crypto_currency import parse_cryptonator
from scripts.parsers.settings import settings
from data.colors import colors


class CryptoCurrency(commands.Cog):
    """Курс криптовалюты (btc, eth и т.д) на сегодня"""

    def __init__(self, bot):
        self.bot = bot

    def cryptocurrency_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}курс\_крипты', value = 'Курс криптовалюты на сегодня', inline = False)

    async def cryptocurrency_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Курс криптовалюты')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}курс_крипты`\n┗ Выведет информацию о курсах криптовалюты', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Курсе криптовалюты на сегодня" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'cryptocurrency', 'crypto_currency',
                                'криптокурс', 'крипто_курс', 'курс_крипты', 'курскрипты', 'курс_криптовалюты', 'курскриптовалюты'
                                ])
    async def cryptocurrency_command(self, ctx):
        emb = discord.Embed(title = f'Курс крипты за {datetime.now(pytz.timezone("Europe/Moscow")).strftime("%d.%m.%Y")}', color = colors['help'])
        parse_cryptonator(emb)
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(self.bot.user))
        emb.set_thumbnail(url = avatar(self.bot.user))
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о курсе криптовалюты — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(CryptoCurrency(bot))