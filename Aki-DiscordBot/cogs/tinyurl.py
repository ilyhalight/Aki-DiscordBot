import discord
import pyshorteners

from discord.ext import commands

from core.bot import avatar
from data.colors import colors
from core.logger import logger
from scripts.parsers.imgs import imgs
from scripts.parsers.settings import settings


class Tiny_url(commands.Cog):
    """Сокращает ссылки"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [
                                'shortlink', 'surl', 'slink', 'shorturl', 'tinylink', 'turl', 'tlink', 'create_tiny_url',
                                'шортлинк',  'сюрл', 'слинк', 'шортюрл',  'тинилинк', 'тюрл', 'тлинк', 'тиниюрл', 'сделать_короткую_ссылку', 'создать_короткую_ссылку'
                                ])
    async def tiny_url_command(self, ctx, link: str = None):
        if link == None:
            emb = discord.Embed(title = 'Помощник - Сокращение ссылок', color = colors['help'])
            emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}тюрл <ссылка>`', inline = False)
            emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}тюрл https://www.youtube.com`\n┗ Вернёт сокращенную ссылку для сайта "https://www.youtube.com".', inline = False)
            emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}тюрл discord.com`\n┗ Вернёт сокращенную ссылку для сайта "https://discord.com".', inline = False)
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(self.bot.user))
            emb.set_thumbnail(url = imgs['tinyurl'])
            await ctx.send(embed = emb)
        else:
            short_link = pyshorteners.Shortener().tinyurl.short(link)
            emb = discord.Embed(title = '', color = colors['help'])
            emb.add_field(name = '<:link:868572405059174533>Первоначальная ссылка', value = f'⠀⠀{link}', inline = False)
            emb.add_field(name = '<:link:868572405059174533>Сокращенная ссылка', value = f'⠀⠀{short_link}', inline = False)
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(self.bot.user))
            emb.set_author(name = 'Ссылка успешно сокращена')
            emb.set_thumbnail(url = imgs['tinyurl'])
            await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(Tiny_url(bot))