import traceback
import discord
from discord.ext import commands

from core.bot import bot, is_owner, avatar
from core.logger import logger
try:
    from scripts.parsers.imgs import imgs
except ImportError:
    logger.error('Не удалось загрузить модуль scripts/parsers/imgs.py - Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
from scripts.parsers.settings import settings
from data.colors import colors

def init_commands():
    @bot.command(aliases = ['загрузить_ког', 'load_cog', 'загрузить_дополнение', 'load_extention'])
    async def load_extension(ctx, extensions=None):
        if is_owner(ctx.author.id) is True:
            if extensions is None:
                emb = discord.Embed(title = 'Помощник - Загрузить_Ког', color = colors['help'])
                emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}загрузить_ког <название_кога>`', inline = False)
                emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}загрузить_ког avatar`\n┗ Загрузит ког "avatar".', inline = False)
                emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}загрузить_ког random`\n┗ Загрузит ког "random".', inline = False)
                emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                emb.set_thumbnail(url = avatar(bot.user))
                await ctx.send(embed = emb)
                logger.info(f'Информация о "загрузить_ког" - Пользователь: {ctx.author} ({ctx.author.id}).')
            else:
                extensions = extensions.lower()
                try:
                    bot.load_extension(f'cogs.{extensions}')
                    emb = discord.Embed(description = f'Ког "{extensions}" успешно загружен\n (с) <@{ctx.author.id}>', color = colors['success'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Успех', icon_url = avatar(ctx.author))
                    if imgs:
                        emb.set_thumbnail(url = imgs['success'])
                    await ctx.send(embed = emb)
                    logger.success(f'Ког "{extensions}" загружен - Пользователь: {ctx.author} ({ctx.author.id}).')
                except commands.ExtensionAlreadyLoaded:
                    emb = discord.Embed(description = f'Ког "{extensions}" уже загружен\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    if imgs:
                        emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось загрузить ког - Причина: Ког "{extensions}" уже загружен - Пользователь: {ctx.author} ({ctx.author.id}).')
                except commands.ExtensionNotFound:
                    emb = discord.Embed(description = f'Ког "{extensions}" не найден\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    if imgs:
                        emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось загрузить ког - Причина: Ког "{extensions}" не найден - Пользователь: {ctx.author} ({ctx.author.id}).')
        elif is_owner(ctx.author.id) == 'Команда отключена из-за ошибки.':
            emb = discord.Embed(description = f'Команда отключена из-за ошибки\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Упс-с', icon_url = avatar(ctx.author))
            if imgs:
                emb.set_thumbnail(url = imgs['not_available'])
            await ctx.send(embed = emb)
            logger.error(f'Не удалось загрузить ког - Причина: Команда отключена из-за ошибки - Пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            if imgs:
                emb.set_thumbnail(url = imgs['no_permissions'])
            await ctx.send(embed = emb)
            logger.error(f'Не удалось загрузить ког - Причина: Недостаточно прав - Пользователь: {ctx.author} ({ctx.author.id}).')

    @bot.command(aliases = ['отгрузить_ког', 'unload_cog', 'отгрузить_дополнение', 'unload_extention', 'выгрузить_ког', 'выгрузить_дополнение'])
    async def unload_extension(ctx, extensions=None):
        if is_owner(ctx.author.id) is True:
            if extensions is None:
                emb = discord.Embed(title = 'Помощник - Выгрузить_Ког', color = colors['help'])
                emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}выгрузить_ког <название_кога>`', inline = False)
                emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}выгрузить_ког avatar`\n┗ Выгрузит ког "avatar".', inline = False)
                emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}выгрузить_ког random`\n┗ Выгрузит ког "random".', inline = False)
                emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                emb.set_thumbnail(url = avatar(bot.user))
                await ctx.send(embed = emb)
                logger.info(f'Информация о "выгрузить_ког" - Пользователь: {ctx.author} ({ctx.author.id}).')
            else:
                extensions = extensions.lower()
                try:
                    bot.unload_extension(f'cogs.{extensions}')
                    emb = discord.Embed(description = f'Ког "{extensions}" успешно выгружен\n (с) <@{ctx.author.id}>', color = colors['success'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Успех', icon_url = avatar(ctx.author))
                    if imgs:
                        emb.set_thumbnail(url = imgs['success'])
                    await ctx.send(embed = emb)
                    logger.success(f'Ког "{extensions}" выгружен - Пользователь: {ctx.author} ({ctx.author.id}).')
                except commands.ExtensionNotFound:
                    emb = discord.Embed(description = f'Ког "{extensions}" не найден\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    if imgs:
                        emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось выгрузить ког - Причина: Ког "{extensions}" не найден - Пользователь: {ctx.author} ({ctx.author.id}).')
                except commands.ExtensionNotLoaded:
                    emb = discord.Embed(description = f'Ког "{extensions}" не загружен\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    if imgs:
                        emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось выгрузить ког - Причина: Ког "{extensions}" не загружен - Пользователь: {ctx.author} ({ctx.author.id}).')
        elif is_owner(ctx.author.id) == 'Команда отключена из-за ошибки.':
            emb = discord.Embed(description = f'Команда отключена из-за ошибки\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Упс-с', icon_url = avatar(ctx.author))
            if imgs:
                emb.set_thumbnail(url = imgs['not_available'])
            await ctx.send(embed = emb)
            logger.error(f'Не удалось выгрузить ког - Причина: Команда отключена из-за ошибки - Пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            if imgs:
                emb.set_thumbnail(url = imgs['no_permissions'])
            await ctx.send(embed = emb)
            logger.error(f'Не удалось выгрузить ког - Причина: Недостаточно прав - Пользователь: {ctx.author} ({ctx.author.id}).')

    @bot.command(aliases = ['перезагрузить_ког', 'reload_cog', 'перезагрузить_дополнение', 'reload_extention'])
    async def reload_extension(ctx, extensions=None):
        if is_owner(ctx.author.id) is True:
            if extensions is None:
                emb = discord.Embed(title = 'Помощник - Перезагрузить_Ког', color = colors['help'])
                emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}перезагрузить_ког <название_кога>`', inline = False)
                emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}перезагрузить_ког avatar`\n┗ Перезагрузит ког "avatar".', inline = False)
                emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}перезагрузить_ког random`\n┗ Перезагрузит ког "random".', inline = False)
                emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                emb.set_thumbnail(url = avatar(bot.user))
                await ctx.send(embed = emb)
                logger.info(f'Информация о "перезагрузить_ког" - Пользователь: {ctx.author} ({ctx.author.id}).')
            else:
                extensions = extensions.lower()
                try:
                    bot.unload_extension(f'cogs.{extensions}')
                    bot.load_extension(f'cogs.{extensions}')
                    emb = discord.Embed(description = f'Ког "{extensions}" успешно перезагружен\n (с) <@{ctx.author.id}>', color = colors['success'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Успех', icon_url = avatar(ctx.author))
                    if imgs:
                        emb.set_thumbnail(url = imgs['success'])
                    await ctx.send(embed = emb)
                    logger.success(f'Ког "{extensions}" перезагружен - Пользователь: {ctx.author} ({ctx.author.id}).')
                except commands.ExtensionNotFound:
                    emb = discord.Embed(description = f'Ког "{extensions}" не найден\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    if imgs:
                        emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось перезагрузить ког - Причина: Ког "{extensions}" не найден - Пользователь: {ctx.author} ({ctx.author.id}).')
                except commands.ExtensionNotLoaded:
                    emb = discord.Embed(description = f'Ког "{extensions}" не загружен\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    if imgs:
                        emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось перезагрузить ког - Причина: Ког "{extensions}" не загружен - Пользователь: {ctx.author} ({ctx.author.id}).')
        elif is_owner(ctx.author.id) == 'Команда отключена из-за ошибки.':
            emb = discord.Embed(description = f'Команда отключена из-за ошибки\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Упс-с', icon_url = avatar(ctx.author))
            if imgs:
                emb.set_thumbnail(url = imgs['not_available'])
            await ctx.send(embed = emb)
            logger.error(f'Не удалось перезагрузить ког - Причина: Команда отключена из-за ошибки - Пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            if imgs:
                emb.set_thumbnail(url = imgs['no_permissions'])
            await ctx.send(embed = emb)
            logger.error(f'Не удалось перезагрузить ког - Причина: Недостаточно прав - Пользователь: {ctx.author} ({ctx.author.id}).')
