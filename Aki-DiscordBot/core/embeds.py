import discord
from core.logger import logger
from core.bot import bot, avatar

from data.colors import colors
from scripts.parsers.imgs import imgs


class Errors():
    async def custom_msg_embed(self, ctx, error_msg = None):
        """Показывает эмбед с кастомной ошибкой"""

        emb = discord.Embed(description = error_msg, color = colors['error'])
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
        emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
        if imgs: emb.set_thumbnail(url = imgs['error'])

        await ctx.send(embed = emb)
        logger.debug(f'Показан эмбед об ошибке "{error_msg}" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

        return True

    async def not_available_embed(self, ctx):
        """Показывает эмбед с ошибкой 'команда отключена из-за ошибки' """

        emb = discord.Embed(description = f'Команда отключена из-за ошибки', color = colors['error'])
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
        emb.set_author(name = 'Упс-с', icon_url = avatar(ctx.author))
        if imgs: emb.set_thumbnail(url = imgs['not_available'])

        await ctx.send(embed = emb)
        logger.debug(f'Показан эмбед c ошибкой "команда отключена из-за ошибки" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

        return True

    async def no_permissions_embed(self, ctx):
        """Показывает эмбед с ошибкой 'недостаточно прав' """

        emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
        emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
        if imgs: emb.set_thumbnail(url = imgs['no_permissions'])

        await ctx.send(embed = emb)
        logger.debug(f'Показан эмбед c ошибкой "недостаточно прав" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

        return True

class Helpers():
    async def default_embed(self, ctx, bot_avatar = None, command_name = None):
        """Показывает стандартный эмбед о помощи по команде"""

        emb = discord.Embed(title = command_name, color = colors['helper'])
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = bot_avatar)
        emb.set_author(name = 'Помощник', icon_url = avatar(ctx.author))
        if imgs: emb.set_thumbnail(url = imgs['help'])

        return emb

    async def custom_image_embed(self, ctx, bot_avatar = None, img = None, command_name = None):
        """Показывает эмбед со своим изображением о помощи по команде"""

        emb = discord.Embed(title = command_name, color = colors['helper'])
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = bot_avatar)
        emb.set_author(name = 'Помощник', icon_url = avatar(ctx.author))
        if imgs: emb.set_thumbnail(url = imgs[img])

        return emb