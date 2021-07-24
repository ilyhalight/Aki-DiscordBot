import discord
import time
import psutil as ps
import platform
import distro
import os
import sys

from discord.ext import commands

from core.bot import avatar
from data.colors import colors
from core.logger import logger



start_time = time.time()
IS_WINDOWS = os.name == 'nt'
IS_MAC = sys.platform == 'darwin'
IS_LINUX = sys.platform == 'linux'
def bytes2Human(number, typer = None): # Thanks Fsoky community
        # Пример Работы Этой Функции перевода чисел:
        # >> bytes2Human(10000)
        # >> '9.8K'
        # >> bytes2Human(100001221)
        # >> '95.4M'

        if typer == "system":
            symbols = ('KБ', 'МБ', 'ГБ', 'TБ', 'ПБ', 'ЭБ', 'ЗБ', 'ИБ')  # Для перевода в Килобайты, Мегабайты, Гигобайты, Террабайты, Петабайты, Петабайты, Эксабайты, Зеттабайты, Йоттабайты
        else:
            symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')  # Для перевода в обычные цифры (10k, 10MM)

        prefix = {}

        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10

        for s in reversed(symbols):
            if number >= prefix[s]:
                value = float(number) / prefix[s]
                return '%.1f%s' % (value, s)

        return f"{number}B"
class Resource(commands.Cog):
    """Shows system information about the bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [
                                'resources', 'resource', 'bot_resources', 'bot_resource',
                                'загруженность', 'загруженностьбота', 'загруженность_бота', 'ресурсы', 'ресурсыбота', 'ресурсы_бота', 'потребление', 'потребление_ресурсов', 'потреблениересурсов'])
    async def resource_analytics_command(self, ctx):
        mem = ps.virtual_memory()
        ping = self.bot.ws.latency

        time_up = time.time() - start_time
        days_up = round(time_up) // 86400
        time_up %= 86400
        hours_up = round(time_up) // 3600
        time_up %= 3600
        minutes_up = round(time_up) // 60
        time_up = round(time_up % 60)
        if days_up == 0 and hours_up == 0 and minutes_up == 0:
            msg = f"**{time_up}** сек. назад"
        elif days_up == 0 and hours_up == 0:
            msg = f"**{minutes_up}** мин. назад"
        elif days_up == 0:
            msg = f"**{hours_up}** час. назад"
        elif days_up > 0:
            msg = f"**{days_up}** дн. назад"
        else:
            msg = f"**{days_up}** дн. **{hours_up}** час. **{minutes_up}** мин. **{time_up}** сек. назад"

        if IS_WINDOWS:
            os_info = platform.uname()
            os_version = f'{os_info.system} {os_info.release}'
        elif IS_MAC:
            os_info = platform.mac_ver()
            os_version = f'Mac OS X {os_info[0]} {os_info[2]}'
        else:
            os_info = distro.linux_distribution()
            os_version = f'{os_info[0]} {os_info[1]}'

        emb = discord.Embed(title = 'Потребление ресурсов', color = colors['help'])
        emb.add_field(name = '<:cpu:868488839671476314>CPU', value = f'⠀⠀{ps.cpu_percent()}%', inline = True)
        emb.add_field(name = '<:ram:868489182383845376>RAM', value = f'⠀⠀{bytes2Human(mem.used, "system")}/{bytes2Human(mem.total, "system")}', inline = True)
        emb.add_field(name = '<:ping:868489884023787580>PING', value = f'⠀⠀{ping * 1000:.0f}ms\n', inline = True)
        emb.add_field(name = '<:os:868494322415312926>OS:', value = f'⠀⠀{os_version}', inline = True)
        emb.add_field(name = '<:start:868490519410511902>LAUNCH:', value = f'⠀⠀{msg}', inline = True)
        emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(self.bot.user))
        emb.set_thumbnail(url = avatar(self.bot.user))
        await ctx.send(embed = emb)
        logger.info(f'Информация о загруженности боте - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Resource(bot))