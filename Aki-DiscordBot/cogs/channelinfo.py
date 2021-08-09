import discord
import datetime

from discord.ext import commands

from data.colors import colors
from core.bot import user_avatar

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

        is_text = channel.type
        if is_text == 'text':
            is_text = 'Текстовый'
        else:
            is_text = 'Голосовой'

        is_nsfw = channel.is_nsfw()
        if is_nsfw == 'nswf ':
            is_nsfw = 'Включен'
        else:
            is_nsfw = 'Выключен'

        channel_created_at = channel.created_at.strftime("%d.%m.%Y, %H:%M:%S UTC")
        emb = discord.Embed(title = f'Информация о канале {channel.name}', color = colors['help'])
        emb.add_field(name = 'Тип', value = is_text, inline = True)
        emb.add_field(name = 'Позиция в категории', value = channel.position, inline = True)
        emb.add_field(name = 'Айди канала', value = channel.id, inline = False)
        emb.add_field(name = 'NSFW', value = is_nsfw, inline = False)
        emb.set_footer(text = f'Канал создан: {channel_created_at}', icon_url = user_avatar(self.bot.user))
        await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(Channelinfo(bot))