import discord

from discord.ext import commands

from core.bot import avatar, is_owner
from core.embeds import Errors, Helpers
from core.logger import logger
from scripts.parsers.settings import settings
from scripts.parsers.status import status, update_status


class BotStatus(commands.Cog):
    """Изменяет статус бота"""

    def __init__(self, bot):
        self.bot = bot

    def botstatus_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}бот\_статус', value = 'Изменить статус бота', inline = False)

    async def botstatus_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Статус бота')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}бот_статус <статус> <активность> <ссылка> <текст>`\n┗ Сменит статус бота на заданный.', inline = False)
        emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}бот_статус онлайн слушает None $help - осн. комманды`\n┗ Сменит статус бота на онлайн, активность на слушает, а текст на "$help - осн.комманды".', inline = False)
        emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}бот_статус идле стримит https://www.twitch.tv/bratishkinoff $help - осн. комманды`\n┗ Сменит статус бота на идле, активность на стримит, а текст на "$help - осн.комманды".', inline = False)
        emb.add_field(name = 'Статусы', value = f'Онлайн, оффлайн, идле, не_беспокоить, невидимка', inline = False)
        emb.add_field(name = 'Активности', value = f'Играет, слушает, смотрит, стримит', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Статусе бота" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'botstatus', 'bot_status',
                                'ботстатус', 'бот_статус'
                                ])
    async def botstatus_command(self, ctx, new_status = None, new_active = None, stream_link = None, *, arg = None):
        if is_owner(ctx.author.id) is True:
            if all((new_active, new_status, stream_link, arg)):
                if new_status.lower() in ['offline', 'оффлайн', 'оффлаин', 'офлайн', 'офлаин', 'не_в_сети', 'офф']:
                    new_status = discord.Status.offline
                elif new_status.lower() in ['idle', 'идле', 'идлэ', 'офлайн', 'офлаин', 'не_активен']:
                    new_status = discord.Status.idle
                elif new_status.lower() in ['dnd', 'днд', 'не_беспокоить']:
                    new_status = discord.Status.dnd
                elif new_status.lower() in ['invisible', 'инвизибл', 'инвизибле', 'невидимка', 'невидимый']:
                    new_status = discord.Status.invisible
                else:
                    new_status = discord.Status.online

                if new_active.lower() in ['play', 'playing', 'играет', 'играть']:
                    new_activity = discord.ActivityType.playing
                elif new_active.lower() in ['listen', 'listening', 'слушает', 'слушать']:
                    new_activity = discord.ActivityType.listening
                elif new_active.lower() in ['watch', 'watching', 'смотрит', 'смотреть']:
                    new_activity = discord.ActivityType.watching
                elif new_active.lower() in ['stream', 'streaming', 'стримит', 'стриметь']:
                    new_activity = discord.ActivityType.streaming
                else:
                    new_activity = discord.ActivityType.custom

                if stream_link.startswith('www.') and new_activity == discord.ActivityType.streaming or stream_link.startswith('http') and new_activity == discord.ActivityType.streaming:
                    await self.bot.change_presence(status = new_status, activity = discord.Activity(name = arg, url = stream_link, type = new_activity))
                    status['status'] = new_status[0]
                    status['active'] = new_activity[1]
                    status['link'] = stream_link
                    status['text'] = arg
                    update_status(status)
                    logger.warning(f'Статус бота изменен — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
                    logger.info(f'Новый Статус: {new_status}, Активность: {new_activity}, Ссылка: {stream_link}, Текст: {arg}')
                else:
                    await self.bot.change_presence(status = new_status, activity = discord.Activity(name = arg, type = new_activity))
                    status['status'] = new_status[0]
                    status['active'] = new_activity[1]
                    status['link'] = stream_link
                    status['text'] = arg
                    update_status(status)
                    logger.warning(f'Статус бота изменен — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
                    logger.info(f'Новый Статус: {new_status}, Активность: {new_activity}, Ссылка: {stream_link}, Текст: {arg}')
            else:
                await self.botstatus_helper(ctx)
        elif is_owner(ctx.author.id) == 'Команда отключена из-за ошибки.':
            await Errors.not_available_embed(self, ctx)
            logger.error(f'Не удалось изменить статус - Причина: Команда отключена из-за ошибки — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await Errors.no_permissions_embed(self, ctx)
            logger.error(f'Не удалось изменить статус - Причина: Недостаточно прав — Запросил пользователь: {ctx.author} ({ctx.author.id}).')


    @botstatus_command.error
    async def botstatus_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await Errors.custom_msg_embed(self, ctx, error)
            logger.error(f'Не удалось изменить статус - Причина: {error} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            logger.error(error)
        else:
            await Errors.custom_msg_embed(self, ctx, error)
            logger.error(error)
def setup(bot):
    bot.add_cog(BotStatus(bot))