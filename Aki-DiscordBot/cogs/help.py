import discord

from discord.ext import commands

from core.bot import is_owner
from core.logger import logger
from data.colors import colors
from scripts.parsers.settings import settings
from scripts.parsers.imgs import imgs

# Импортируем все коги, где определна функция ***_help
from cogs.avatar import Avatar
from cogs.bot_info import BotInfo
from cogs.bot_status import BotStatus
from cogs.channel_info import ChannelInfo
from cogs.crypto_currency import CryptoCurrency
from cogs.csgo_give_privillege import CSGOGivePrivillege
from cogs.csgo_remove_privillege import CSGORemovePrivillege
from cogs.currency import Currency
from cogs.giveaway import Giveaway
from cogs.random import Random
from cogs.reactions import Reactions
from cogs.resource import Resource
from cogs.tiny_url import TinyUrl


class Help(commands.Cog):
    """Показывает список всех команд"""

    def __init__(self, bot):
        self.bot = bot

    async def help_default_message(self, ctx):
        emb = discord.Embed(title = f'Доступные команды:', description = f'**Префикс: `{settings["prefix"]}`**', color = colors['help'])
        emb.add_field(name = f'Информация ({settings["prefix"]}хелп Информация)', value = '`В данном разделе содержатся все информационные команды`', inline = False)
        emb.add_field(name = f'Модерация ({settings["prefix"]}хелп Модерация)', value = '`В этом разделе собраны все команды администратора`', inline = False)
        emb.add_field(name = f'Действия ({settings["prefix"]}хелп Действия)', value = '`В данном разделе содержатся все РП команды`', inline = False)
        emb.add_field(name = f'Весёлое ({settings["prefix"]}хелп Весёлое)', value = '`В данном разделе содержатся все весёлые команды`', inline = False)
        emb.add_field(name = f'Утилиты ({settings["prefix"]}хелп Утилиты)', value = '`В данном разделе содержатся все утилиты`', inline = False)
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
        emb.set_thumbnail(url = imgs['help'])
        await ctx.send (embed = emb)
        logger.info(f'Выведена информация о "Всех командах" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    def help_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}хелп', value = 'Информация о командах', inline = False)

    @commands.command(aliases = [
                                'help', 'commands',
                                'хелп', 'команды', 'комманды'
                                ])
    async def help_command(self, ctx, title: str = None):
        """Вывод списка доступных команд

        Args:
            title (str): Название категории

        Returns:
            Embed - success
        """
        if title is None:
            await self.help_default_message(ctx)
        elif title.lower() in ['информация', 'инфо', 'info', 'information', 'informations']:
            emb = discord.Embed(title = f'Доступные команды группы `Информация`:', description = f'**Префикс: `{settings["prefix"]}`**', color = colors['help'])

            try:
                self.help_help(settings["prefix"], emb)
                BotInfo.botinfo_help(self, settings["prefix"], emb)
                ChannelInfo.channelinfo_help(self, settings["prefix"], emb)
                Resource.resource_help(self, settings["prefix"], emb)
            except:
                emb.add_field(name = f'Ошибка', value = 'Не удалось загрузить команды', inline = False)

            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            if imgs: emb.set_thumbnail(url = imgs['help'])
            await ctx.send (embed = emb)
            logger.info(f'Выведена информация о "Доступных командах группы `Информация`" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

        elif title.lower() in ['модерация', 'модер', 'администрирование', 'администратор', 'админ', 'moderation', 'moder', 'administration', 'administrator', 'admin']:
            emb = discord.Embed(title = f'Доступные команды группы `Модерация`:', description = f'**Префикс: `{settings["prefix"]}`**', color = colors['help'])

            try:
                Giveaway.giveaway_help(self, settings["prefix"], emb)
                Reactions.reactions_help(self, settings["prefix"], emb)
            except:
                emb.add_field(name = f'Ошибка', value = 'Не удалось загрузить команды', inline = False)

            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            if imgs: emb.set_thumbnail(url = imgs['help'])
            await ctx.send (embed = emb)
            logger.info(f'Выведена информация о "Доступных командах группы `Модерация`" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

        elif title.lower() in ['действия', 'действие', 'деиствия', 'деиствие', 'ролеплеи', 'роле_плеи', 'ролеплей', 'рп', 'роле_плей', 'actions', 'action', 'roleplay', 'rp', 'role_play']:
            emb = discord.Embed(title = f'Доступные команды группы `Действия`:', description = f'**Префикс: `{settings["prefix"]}`**', color = colors['help'])

            try:
                emb.add_field(name = 'Упс-с', value = 'Здесь, пока что, ничего нет', inline = False)
            except:
                emb.add_field(name = f'Ошибка', value = 'Не удалось загрузить команды', inline = False)

            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            if imgs: emb.set_thumbnail(url = imgs['help'])
            await ctx.send (embed = emb)
            logger.info(f'Выведена информация о "Доступных командах группы `Действия`" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

        elif title.lower() in ['весёлое', 'веселое', 'happy', 'happies', 'funny']:
            emb = discord.Embed(title = f'Доступные команды группы `Весёлое`:', description = f'**Префикс: `{settings["prefix"]}`**', color = colors['help'])

            try:
                emb.add_field(name = 'Упс-с', value = 'Здесь, пока что, ничего нет', inline = False)
            except:
                emb.add_field(name = f'Ошибка', value = 'Не удалось загрузить команды', inline = False)

            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            if imgs: emb.set_thumbnail(url = imgs['help'])
            await ctx.send (embed = emb)
            logger.info(f'Выведена информация о "Доступных командах группы `Весёлое`" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

        elif title.lower() in ['утилиты', 'utility', 'utillity', 'utilities']:
            emb = discord.Embed(title = f'Доступные команды группы `Утилиты`:', description = f'**Префикс: `{settings["prefix"]}`**', color = colors['help'])

            try:
                Avatar.avatar_help(self, settings["prefix"], emb)
                Random.random_help(self, settings["prefix"], emb)
                CryptoCurrency.cryptocurrency_help(self, settings["prefix"], emb)
                Currency.currency_help(self, settings["prefix"], emb)
                TinyUrl.tinyurl_help(self, settings["prefix"], emb)
            except:
                emb.add_field(name = f'Ошибка', value = 'Не удалось загрузить команды', inline = False)

            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            if imgs: emb.set_thumbnail(url = imgs['help'])
            await ctx.send (embed = emb)
            logger.info(f'Выведена информация о "Доступных командах группы `Утилиты`" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

        elif is_owner(ctx.author.id) is True and title.lower() in ['owner', 'владелец']:
            emb = discord.Embed(title = f'Доступные команды группы `Утилиты`:', description = f'**Префикс: `{settings["prefix"]}`**', color = colors['help'])

            try:
                BotStatus.botstatus_help(self, settings["prefix"], emb)
                CSGOGivePrivillege.csgo_give_privillege_help(self, settings["prefix"], emb)
                CSGORemovePrivillege.csgo_remove_privillege_help(self, settings["prefix"], emb)
            except:
                emb.add_field(name = f'Ошибка', value = 'Не удалось загрузить команды', inline = False)

            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            if imgs: emb.set_thumbnail(url = imgs['help'])
            await ctx.send (embed = emb)
            logger.info(f'Выведена информация о "Доступных командах группы `Утилиты`" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await self.help_default_message(ctx)

def setup(bot):
    bot.add_cog(Help(bot))