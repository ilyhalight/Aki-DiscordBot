import discord
from discord.ext import commands

from core.bot import avatar, is_owner
from data.colors import colors
from core.logger import logger
from scripts.parsers.settings import settings
from scripts.parsers.imgs import imgs


class Botstatus(commands.Cog):
    """Изменяет статус бота"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [
                                'botstatus', 'bot_status',
                                'ботстатус', 'бот_статус'
                                ])
    async def botstatus_command(self, ctx, status = None, active = None, stream_link = None, *, arg = None):
        if is_owner(ctx.author.id):
            if status is not None and active is not None and stream_link is not  None and arg is not None:
                if status.lower() in ['offline', 'оффлайн', 'оффлаин', 'офлайн', 'офлаин', 'не_в_сети']:
                    new_status = discord.Status.offline
                elif status.lower() in ['idle', 'идле', 'идлэ', 'офлайн', 'офлаин', 'не_активен']:
                    new_status = discord.Status.idle
                elif status.lower() in ['dnd', 'днд', 'не_беспокоить']:
                    new_status = discord.Status.dnd
                elif status.lower() in ['invisible', 'инвизибл', 'инвизибле', 'невидимка', 'невидимый']:
                    new_status = discord.Status.invisible
                else:
                    new_status = discord.Status.online

                if active.lower() in ['listen', 'listening', 'слушает', 'слушать']:
                    new_activity = discord.ActivityType.listening
                elif active.lower() in ['watch', 'watching', 'смотрит', 'смотреть']:
                    new_activity = discord.ActivityType.watching
                else:
                    new_activity = discord.ActivityType.streaming

                if stream_link.startswith('www.') and new_activity == discord.ActivityType.streaming or stream_link.startswith('http') and new_activity == discord.ActivityType.streaming:
                    await self.bot.change_presence(status = new_status, activity = discord.Activity(name = arg, url = stream_link, type = new_activity))
                    logger.warning(f'Статус бота изменен - Пользователь: {ctx.author} ({ctx.author.id}).')
                    logger.info(f'Новый Статус: {new_status}, Активность: {new_activity}, Ссылка: {stream_link}, Текст: {arg}')
                else:
                    await self.bot.change_presence(status = new_status, activity = discord.Activity(name = arg, type = new_activity))
                    logger.warning(f'Статус бота изменен - Пользователь: {ctx.author} ({ctx.author.id}).')
                    logger.info(f'Новый Статус: {new_status}, Активность: {new_activity}, Ссылка: {stream_link}, Текст: {arg}')
            else:
                emb = discord.Embed(title = 'Помощник - Бот статус', color = colors['help'])
                emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}бот_статус <статус> <активность> <ссылка> <текст>`', inline = False)
                emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}бот_статус онлайн слушает нет $help - осн.комманды`\n┗ Сменит статус бота на онлайн, активность на слушает, а текст на "$help - осн.комманды".', inline = False)
                emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}бот_статус идле стримит https://www.twitch.tv/bratishkinoff $help - осн.комманды`\n┗ Сменит статус бота на идле, активность на стримит, а текст на "$help - осн.комманды".', inline = False)
                emb.add_field(name = 'Статусы', value = f'Онлайн, оффлайн, идле, не_беспокоить, невидимка', inline = False)
                emb.add_field(name = 'Активность', value = f'Онлайн, оффлайн, идле, не_беспокоить, невидимка', inline = False)
                emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(self.bot.user))
                emb.set_thumbnail(url = avatar(self.bot.user))
                await ctx.send(embed = emb)
                logger.info(f'Информация о "бот_статус" - Пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            emb = discord.Embed(description = f'Недостаточно прав\n (с) <@{ctx.author.id}>', color = colors['error'])
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(self.bot.user))
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            emb.set_thumbnail(url = imgs['no_permissions'])
            await ctx.send(embed = emb)
            logger.error(f'Не удалось изменить статус - Причина: Недостаточно прав - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Botstatus(bot))