import discord

from discord.ext import commands
from core.embeds import Errors, Helpers

from data.colors import colors
from core.bot import avatar, bot
from core.logger import logger
from scripts.parsers.settings import settings
from scripts.parsers.emojis import emojis

channels = {
    'voice': 'Голосовой',
    'text': 'Текстовый',
    'private': 'Приватный',
    'group': 'Групповой',
    'category': 'Категории',
    'news': 'Новостной',
    'store': 'Магазин',
    'stage_voice': 'Сценический'
}

emoji = emojis['channel_info']


class ChannelInfo(commands.Cog):
    """Показывает информацию о канале c заданным ID"""

    def __init__(self, bot):
        self.bot = bot

    def channelinfo_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}канал', value = 'Информация о канале c заданным ID', inline = False)

    async def channelinfo_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Информация о канале')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}канал [id канала]`\n┗ Выведет информацию о канале с заданным ID.', inline = False)
        emb.add_field(name = 'Примечание', value = f'Бот может вывести информацию о каналах, только, текущего сервера', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Информация о канале" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'cinfo', 'channel_info', 'channelinfo', 'about_channel', 'aboutchannel', 'channel'
                                'кинфо', 'канал_инфо', 'каналинфо', 'о_канале', 'оканале', 'канал'
                                ])
    async def channelinfo_command(self, ctx, channel_id: int = None):
        if channel_id is not None and type(channel_id) is int:
            channel = bot.get_channel(channel_id)
        else:
            channel = ctx.message.channel

        try:
            channel_type = channels.get(str(channel.type))
        except AttributeError as err:
            logger.error(f'Произошла ошибка с каналом {channel}! Причина ошибки: {err}')
            raise
        logger.debug(f'Получена информация о канале {channel.id}. Название: "{channel.name}", Тип: "{channel.type}", Категория: "{channel.category}" % Сервер: {channel.guild.name} ({channel.guild.id}), Участники сервера: {channel.guild.member_count} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        emb = discord.Embed(title = f'Информация о канале', color = colors['help'])


        channel_created_at = channel.created_at.strftime("%d.%m.%Y, %H:%M:%S UTC")
        emb.add_field(name = 'Название', value = channel.mention, inline = True)
        emb.add_field(name = 'ID', value = channel.id, inline = True)

        if channel.category is not None: emb.add_field(name = 'В категории', value = channel.category, inline = True)
        if str(channel.type) == 'text':
            channel_type_emoji = emoji['text']
            if channel.slowmode_delay is not None and channel.slowmode_delay != 0:
                emb.add_field(name = 'Медленный режим', value = f'{channel.slowmode_delay} сек.', inline = True)
            if channel.is_nsfw() == True and channel.is_news() == True:
                channel_type = f'Новостной NSFW'
                channel_type_emoji = emoji['news_nsfw']
            elif channel.is_nsfw() == True and channel.is_news() == False:
                channel_type = f'{channel_type} NSFW'
                channel_type_emoji = emoji['text_nsfw']
            elif channel.is_nsfw() == False and channel.is_news() == True:
                channel_type = f'Новостной'
                channel_type_emoji = emoji['news']

        elif str(channel.type) == 'voice' or str(channel.type) == 'stage':
            if str(channel.type) == 'voice':
                channel_type_emoji = emoji['voice']
            else:
                channel_type_emoji = emoji['stage']
            bitrate = str(channel.bitrate)

            emb.add_field(name = 'Битрейт', value = f'{bitrate[:-3]} кбит/c', inline = True)
            if channel.rtc_region is not None:
                emb.add_field(name = 'Регион', value = channel.rtc_region, inline = True)
            else:
                emb.add_field(name = 'Регион', value = 'Авто', inline = True)
            if int(channel.user_limit) != 0:
                emb.add_field(name = 'Лимит', value = channel.user_limit, inline = True)
            if int(len(channel.voice_states)) != 0:
                emb.add_field(name = 'Участники', value = len(channel.voice_states), inline = True)

        elif str(channel.type) == 'store':
            channel_type_emoji = emoji['store']

        else:
            channel_type_emoji = ' '

        emb.add_field(name = f'Тип', value = f'{channel_type_emoji} {channel_type}', inline = True)
        emb.set_footer(text = f'Канал создан: {channel_created_at}', icon_url = avatar(self.bot.user))
        await ctx.send(embed = emb)


    @channelinfo_command.error
    async def channelinfo_command_error(self, ctx, error):
        if isinstance (error, commands.CommandInvokeError):
            await Errors.custom_msg_embed(self, ctx, 'Канал не найден')
            logger.error(f'Не удалось показать инофрмацию о канале - Причина: Канал не найден — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            logger.error(error)
        else:
            logger.error(error)

def setup(bot):
    bot.add_cog(ChannelInfo(bot))