import discord

from core.bot import bot

class Cogs():
    def init_commands():
        @bot.command(aliases = ['load', 'load_extension', 'load_extensions', 'load_cog', 'load_cogs', 'загрузить', 'загрузить_ког'])
        async def _commandLoadExtensions(ctx, extensions):
            extensions = extensions.lower()
            if is_owner(ctx.author.id):
                bot.load_extension(f'cogs.{extensions}')
                await ctx.send('Cogs is loaded...')
            else:
                emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = COLOR['no_permissions'])
                emb.set_footer(text = lang['copyright'], icon_url = user_avatar(bot.user))
                emb.set_author(name = 'Ошибка', icon_url = user_avatar(ctx.author))
                emb.set_thumbnail(url = LINK['no_permissions_img'])
                await ctx.send(embed = emb)
                logger.warning(f'Недостаточно прав - Пользователь {ctx.author} попытался сделать бэкап.')

        @bot.command(aliases = ['unload', 'unload_extension', 'unload_extensions', 'unload_cog', 'unload_cogs', 'отгрузить', 'отгрузить_ког'])
        async def _commandUnloadExtensions(ctx, extensions):
            extensions = extensions.lower()
            if is_owner(ctx.author.id):
                bot.unload_extension(f'cogs.{extensions}')
                await ctx.send('Cogs is unloaded...')
            else:
                emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = COLOR['no_permissions'])
                emb.set_footer(text = lang['copyright'], icon_url = user_avatar(bot.user))
                emb.set_author(name = 'Ошибка', icon_url = user_avatar(ctx.author))
                emb.set_thumbnail(url = LINK['no_permissions_img'])
                await ctx.send(embed = emb)
                logger.warning(f'Недостаточно прав - Пользователь {ctx.author} попытался сделать бэкап.')

        @bot.command(aliases = ['reload', 'reload_extension', 'reload_extensions', 'reload_cog', 'reload_cogs', 'перезагрузить', 'перезагрузить_ког'])
        async def _commandReloadExtensions(ctx, extensions):
            extensions = extensions.lower()
            if is_owner(ctx.author.id):
                bot.unload_extension(f'cogs.{extensions}')
                bot.load_extension(f'cogs.{extensions}')
                await ctx.send('Cogs is restarted...')
            else:
                emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = COLOR['no_permissions'])
                emb.set_footer(text = lang['copyright'], icon_url = user_avatar(bot.user))
                emb.set_author(name = 'Ошибка', icon_url = user_avatar(ctx.author))
                emb.set_thumbnail(url = LINK['no_permissions_img'])
                await ctx.send(embed = emb)
                logger.warning(f'Недостаточно прав - Пользователь {ctx.author} попытался сделать бэкап.')