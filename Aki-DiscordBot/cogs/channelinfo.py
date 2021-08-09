import discord
import datetime

from discord.ext import commands

from data.colors import colors
from core.bot import avatar

class Channelinfo(commands.Cog):
    """Показывает информацию о канале"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [
                                'cinfo', 'channel_info', 'channelinfo',
                                'кинфо', 'канал_инфо', 'каналинфо'
                                ])
    async def channel_info_command(self, ctx):
        channel = ctx.message.channel

        channel_type = channel.type
        if channel_type == 'voice':
            channel_type = 'Голосовой'
        elif channel_type == 'private':
            channel_type = 'Приватный'
        elif channel_type == 'group':
            channel_type = 'Групповой'
        elif channel_type == 'category':
            channel_type = 'Категории'
        elif channel_type == 'news':
            channel_type = 'Новостной'
        elif channel_type == 'store':
            channel_type = 'Магазин'
        elif channel_type == 'stage_voice':
            channel_type = 'Сценический'
        else:
            channel_type = 'Текстовый'

        is_nsfw = channel.is_nsfw()
        if is_nsfw == True:
            is_nsfw = 'Включен'
        else:
            is_nsfw = 'Выключен'

        channel_created_at = channel.created_at.strftime("%d.%m.%Y, %H:%M:%S UTC")
        emb = discord.Embed(title = f'Информация о канале {channel.name}', color = colors['help'])
        emb.add_field(name = 'Тип', value = channel_type, inline = True)
        emb.add_field(name = 'Позиция в категории', value = channel.position, inline = True)
        emb.add_field(name = 'Айди канала', value = channel.id, inline = False)
        emb.add_field(name = 'NSFW', value = is_nsfw, inline = False)
        emb.set_footer(text = f'Канал создан: {channel_created_at}', icon_url = avatar(self.bot.user))
        await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(Channelinfo(bot))