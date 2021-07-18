import discord
from discord.ext import commands

from core.bot import bot, is_owner, avatar
from scripts.parsers.imgs import imgs
from scripts.parsers.settings import settings
from data.colors import colors

def init_commands():
    @bot.command(aliases = ['загрузить_ког', 'load_cog', 'загрузить_дополнение', 'load_extention'])
    async def load_extension(ctx, extensions):
        extensions = extensions.lower()
        if is_owner(ctx.author.id):
            if extensions != None:
                try:
                    bot.load_extension(f'cogs.{extensions}')
                    emb = discord.Embed(description = f'Ког "{extensions}" успешно загружен\n (с) <@{ctx.author.id}>', color = colors['success'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Успех', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['success'])
                    await ctx.send(embed = emb)
                except commands.ExtensionAlreadyLoaded:
                    emb = discord.Embed(description = f'Ког "{extensions}" уже загружен\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                except commands.ExtensionNotFound:
                    emb = discord.Embed(description = f'Ког "{extensions}" не найден\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
            else:
                emb = discord.Embed(description = f'Введите **{settings["prefix"]}load <название_кога>**', color = colors['success'])
                emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                emb.set_author(name = 'Использование:', icon_url = avatar(ctx.author))
                emb.set_thumbnail(url = imgs['help'])
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['no_permissions'])
            await ctx.send(embed = emb)
            # logger.warning(f'Недостаточно прав - Пользователь {ctx.author} попытался сделать бэкап.')

    @bot.command(aliases = ['отгрузить_ког', 'unload_cog', 'отгрузить_дополнение', 'unload_extention', 'выгрузить_ког', 'выгрузить_дополнение'])
    async def unload_extension(ctx, extensions):
        extensions = extensions.lower()
        if is_owner(ctx.author.id):
            if extensions != None:
                try:
                    bot.unload_extension(f'cogs.{extensions}')
                    emb = discord.Embed(description = f'Ког "{extensions}" успешно выгружен\n (с) <@{ctx.author.id}>', color = colors['success'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Успех', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['success'])
                    await ctx.send(embed = emb)
                except commands.ExtensionNotFound:
                    emb = discord.Embed(description = f'Ког "{extensions}" не найден\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                except commands.ExtensionNotLoaded:
                    emb = discord.Embed(description = f'Ког "{extensions}" не загружен\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
            else:
                emb = discord.Embed(description = f'Введите **{settings["prefix"]}unload <название_кога>**', color = colors['success'])
                emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                emb.set_author(name = 'Использование:', icon_url = avatar(ctx.author))
                emb.set_thumbnail(url = imgs['help'])
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['no_permissions'])
            await ctx.send(embed = emb)
            # logger.warning(f'Недостаточно прав - Пользователь {ctx.author} попытался сделать бэкап.')

    @bot.command(aliases = ['перегрузить_ког', 'reload_cog', 'перегрузить_дополнение', 'reload_extention'])
    async def reload_extension(ctx, extensions=None):
        extensions = extensions.lower()
        if is_owner(ctx.author.id):
            if extensions != None:
                try:
                    bot.unload_extension(f'cogs.{extensions}')
                    bot.load_extension(f'cogs.{extensions}')
                    await ctx.send('Cogs is restarted.')
                except commands.ExtensionNotFound:
                    emb = discord.Embed(description = f'Ког "{extensions}" не найден\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
                except commands.ExtensionNotLoaded:
                    emb = discord.Embed(description = f'Ког "{extensions}" не загружен\n (с) <@{ctx.author.id}>', color = colors['error'])
                    emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    await ctx.send(embed = emb)
            else:
                emb = discord.Embed(description = f'Введите **{settings["prefix"]}reload <название_кога>**', color = colors['success'])
                emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
                emb.set_author(name = 'Использование:', icon_url = avatar(ctx.author))
                emb.set_thumbnail(url = imgs['help'])
                await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['no_permissions'])
            await ctx.send(embed = emb)
            # logger.warning(f'Недостаточно прав - Пользователь {ctx.author} попытался сделать бэкап.')
