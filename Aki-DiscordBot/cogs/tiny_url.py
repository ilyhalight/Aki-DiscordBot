import discord
import pyshorteners

from discord.ext import commands

from core.bot import avatar
from core.embeds import Helpers
from data.colors import colors
from core.logger import logger
from scripts.parsers.imgs import imgs
from scripts.parsers.settings import settings
from scripts.parsers.emojis import emojis

emoji = emojis['reactions']


class TinyUrl(commands.Cog):
    """Сокращает ссылки"""

    def __init__(self, bot):
        self.bot = bot

    def tinyurl_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}тюрл', value = 'Сократить ссылку', inline = False)

    async def tinyurl_helper(self, ctx):
        emb = await Helpers.custom_image_embed(self, ctx, self.bot.user.avatar_url, 'tinyurl', 'Сокращение ссылок')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}тюрл <ссылка>`', inline = False)
        emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}тюрл https://www.youtube.com`\n┗ Вернёт сокращенную ссылку для сайта "https://www.youtube.com".', inline = False)
        emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}тюрл discord.com`\n┗ Вернёт сокращенную ссылку для сайта "https://discord.com".', inline = False)   
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "тюрл" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'shortlink', 'surl', 'slink', 'shorturl', 'tinylink', 'turl', 'tlink', 'create_tiny_url',
                                'шортлинк',  'сюрл', 'слинк', 'шортюрл',  'тинилинк', 'тюрл', 'тлинк', 'тиниюрл', 'сделать_короткую_ссылку', 'создать_короткую_ссылку'
                                ])
    async def tinyurl_command(self, ctx, link: str = None):
        if link is None or type(link) is not str:
            await self.tinyurl_helper(ctx)
        else:
            short_link = pyshorteners.Shortener().tinyurl.short(link)
            emb = discord.Embed(title = '', color = colors['help'])
            emb.add_field(name = f'{emoji["link"]} Первоначальная ссылка', value = f'⠀⠀{link}', inline = True)
            emb.add_field(name = f'{emoji["link"]} Сокращенная ссылка', value = f'⠀⠀{short_link}', inline = True)
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(self.bot.user))
            emb.set_author(name = 'Ссылка успешно сокращена', icon_url = ctx.author.avatar_url)
            emb.set_thumbnail(url = imgs['tinyurl'])
            await ctx.send(embed = emb)
            logger.success(f'Ссылка "{link}" была сокращена - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(TinyUrl(bot))