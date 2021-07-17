import discord

from core.bot import bot, is_owner, avatar
from scripts.parsers.imgs import imgs
from data.colors import colors

def init_commands():
    @bot.command(aliases = ['загрузить_ког', 'load_cog', 'загрузить_дополнение', 'load_extention'])
    async def _commandLoadExtensions(ctx, extensions):
        extensions = extensions.lower()
        if is_owner(ctx.author.id):
            bot.load_extension(f'cogs.{extensions}')
            await ctx.send('Cogs is loaded.')
        else:
            emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['no_permissions'])
            await ctx.send(embed = emb)
            # logger.warning(f'Недостаточно прав - Пользователь {ctx.author} попытался сделать бэкап.')

    @bot.command(aliases = ['отгрузить_ког', 'unload_cog', 'отгрузить_дополнение', 'unload_extention'])
    async def _commandUnloadExtensions(ctx, extensions):
        extensions = extensions.lower()
        if is_owner(ctx.author.id):
            bot.unload_extension(f'cogs.{extensions}')
            await ctx.send('Cogs is unloaded.')
        else:
            emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['no_permissions'])
            await ctx.send(embed = emb)
            # logger.warning(f'Недостаточно прав - Пользователь {ctx.author} попытался сделать бэкап.')

    @bot.command(aliases = ['перегрузить_ког', 'reload_cog', 'перегрузить_дополнение', 'reload_extention'])
    async def _commandReloadExtensions(ctx, extensions):
        extensions = extensions.lower()
        if is_owner(ctx.author.id):
            bot.unload_extension(f'cogs.{extensions}')
            bot.load_extension(f'cogs.{extensions}')
            await ctx.send('Cogs is restarted.')
        else:
            emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['no_permissions'])
            await ctx.send(embed = emb)
            # logger.warning(f'Недостаточно прав - Пользователь {ctx.author} попытался сделать бэкап.')
