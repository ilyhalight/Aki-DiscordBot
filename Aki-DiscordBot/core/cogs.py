import discord
from discord.ext import commands

from core.bot import bot, is_owner, avatar
from core.logger import logger, logger_help
from scripts.parsers.imgs import imgs
from scripts.parsers.settings import settings
from data.colors import colors

def init_commands():
    @bot.command(aliases = ['загрузить_ког', 'load_cog', 'загрузить_дополнение', 'load_extention'])
    async def load_extension(ctx, extensions=None):
        if extensions is None:
            emb = discord.Embed(description = f'Введите **{settings["prefix"]}load*_*cog <название_кога>**', color = colors['help'])
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Использование', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['help'])
            await ctx.send(embed = emb)
            logger.info(f'Информация о "загрузить_ког" - Пользователь: {ctx.author}.')
        else:
            extensions = extensions.lower()
            if is_owner(ctx.author.id):
                try:
                    bot.load_extension(f'cogs.{extensions}')
                    emb = discord.Embed(description = f'Ког "{extensions}" успешно загружен\n (с) <@{ctx.author.id}>', color = colors['success'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Успех', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['success'])
                    await ctx.send(embed = emb)
                    logger.success(f'Ког {extensions} загружен - Пользователь: {ctx.author}.')
                except commands.ExtensionAlreadyLoaded:
                    emb = discord.Embed(description = f'Ког "{extensions}" уже загружен\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось загрузить ког - Причина: Ког "{extensions}" уже загружен - Пользователь: {ctx.author}.')
                except commands.ExtensionNotFound:
                    emb = discord.Embed(description = f'Ког "{extensions}" не найден\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось загрузить ког - Причина: Ког "{extensions}" не найден - Пользователь: {ctx.author}.')
            else:
                emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
                emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                emb.set_thumbnail(url = imgs['no_permissions'])
                await ctx.send(embed = emb)
                logger.error(f'Не удалось загрузить ког - Причина: Недостаточно прав - Пользователь: {ctx.author}.')

    @bot.command(aliases = ['отгрузить_ког', 'unload_cog', 'отгрузить_дополнение', 'unload_extention', 'выгрузить_ког', 'выгрузить_дополнение'])
    async def unload_extension(ctx, extensions=None):
        if extensions is None:
            emb = discord.Embed(description = f'Введите **{settings["prefix"]}unload*_*cog <название_кога>**', color = colors['help'])
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Использование:', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['help'])
            await ctx.send(embed = emb)
            logger.info(f'Информация о "отгрузить_ког" - Пользователь: {ctx.author}.')
        else:
            extensions = extensions.lower()
            if is_owner(ctx.author.id):
                try:
                    bot.unload_extension(f'cogs.{extensions}')
                    emb = discord.Embed(description = f'Ког "{extensions}" успешно выгружен\n (с) <@{ctx.author.id}>', color = colors['success'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Успех', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['success'])
                    await ctx.send(embed = emb)
                    logger.success(f'Ког {extensions} выгружен - Пользователь: {ctx.author}.')
                except commands.ExtensionNotFound:
                    emb = discord.Embed(description = f'Ког "{extensions}" не найден\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось выгрузить ког - Причина: Ког "{extensions}" не найден - Пользователь: {ctx.author}.')
                except commands.ExtensionNotLoaded:
                    emb = discord.Embed(description = f'Ког "{extensions}" не загружен\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось выгрузить ког - Причина: Ког "{extensions}" не загружен - Пользователь: {ctx.author}.')
            else:
                emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
                emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                emb.set_thumbnail(url = imgs['no_permissions'])
                await ctx.send(embed = emb)
                logger.error(f'Не удалось выгрузить ког - Причина: Недостаточно прав - Пользователь: {ctx.author}.')

    @bot.command(aliases = ['перезагрузить_ког', 'reload_cog', 'перезагрузить_дополнение', 'reload_extention'])
    async def reload_extension(ctx, extensions=None):
        if extensions is None:
            emb = discord.Embed(description = f'Введите **{settings["prefix"]}reload*_*cog <название_кога>**', color = colors['help'])
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Использование:', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['help'])
            await ctx.send(embed = emb)
            logger.info(f'Информация о "перезагрузить_ког" - Пользователь: {ctx.author}.')
        else:
            extensions = extensions.lower()
            if is_owner(ctx.author.id):
                try:
                    bot.unload_extension(f'cogs.{extensions}')
                    bot.load_extension(f'cogs.{extensions}')
                    emb = discord.Embed(description = f'Ког "{extensions}" успешно перезагружен\n (с) <@{ctx.author.id}>', color = colors['success'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Успех', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['success'])
                    await ctx.send(embed = emb)
                    logger.success(f'Ког {extensions} перезагружен - Пользователь: {ctx.author}.')
                except commands.ExtensionNotFound:
                    emb = discord.Embed(description = f'Ког "{extensions}" не найден\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось перезагрузить ког - Причина: Ког "{extensions}" не найден - Пользователь: {ctx.author}.')
                except commands.ExtensionNotLoaded:
                    emb = discord.Embed(description = f'Ког "{extensions}" не загружен\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось перезагрузить ког - Причина: Ког "{extensions}" не загружен - Пользователь: {ctx.author}.')
            else:
                emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
                emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                emb.set_thumbnail(url = imgs['no_permissions'])
                await ctx.send(embed = emb)
                logger.error(f'Не удалось перезагрузить ког - Причина: Недостаточно прав - Пользователь: {ctx.author}.')
