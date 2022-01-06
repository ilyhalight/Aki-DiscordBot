import discord
import time
import psutil as ps
import platform
import distro

from discord.ext import commands

from core.bot import avatar
from core.logger import logger
from data.colors import colors
from scripts.checks import is_windows, is_mac


start_time = time.time() # Получаем текущее unix время при запуске бота

class Resource(commands.Cog):
    """Показывает информацию о потребление ресурсов ботом"""

    def __init__(self, bot):
        self.bot = bot

    async def bytes_to_human(self, number):
        """Переводит число из байтов в максимально возможную систему счисления и присваивает её символ
        Спасибо за логику работы Fsoky Сommunity (Сейчас, Fadager Community) >>> код из осени 2020 года

        Args:
            number: Число байтов

        Return:
            value + symbol (str): Возвращает число, в понятной человеку системе счисления - Успех
            value + Byte (str): Возвращает число, в байтах - Неудача

        Example:
        >> bytes_to_human(10000)
        >> '9.8KБ'
        >> bytes_to_human(100001221)
        >> '95.4MБ'
        """

        symbols = ('KБ', 'МБ', 'ГБ', 'TБ', 'ПБ', 'ЭБ', 'ЗБ', 'ИБ') # Название единиц измерения
        prefix = {}

        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10

        for s in reversed(symbols):
            if number >= prefix[s]:
                value = float(number) / prefix[s]
                return '%.1f%s' % (value, s)

        return f"{number}B"

    @commands.command(aliases = [
                                'resources', 'resource', 'bot_resources', 'bot_resource', 'res',
                                'загруженность', 'загруженностьбота', 'загруженность_бота', 'ресурсы', 'ресурсыбота', 'ресурсы_бота', 'потребление', 'потребление_ресурсов', 'потреблениересурсов'])
    async def resource_command(self, ctx):
        mem = ps.virtual_memory()
        ping = self.bot.ws.latency

        mem_used = await self.bytes_to_human(mem.used)
        mem_total = await self.bytes_to_human(mem.total)

        time_up = time.time() - start_time
        logger.debug(f'Общее время работы бота в секундах: {time_up}')
        days_up = round(time_up) // 86400
        time_up %= 86400
        hours_up = round(time_up) // 3600
        time_up %= 3600
        minutes_up = round(time_up) // 60
        time_up = round(time_up % 60)
        logger.debug(f'Текущее время работы бота в днях: {days_up}, в часах: {hours_up}, в минутах: {minutes_up}, в секундах: {time_up}')

        if all((days_up, hours_up, minutes_up)):
            msg = f"**{days_up}** дн. **{hours_up}** час. **{minutes_up}** мин. **{time_up}** сек. назад"
        elif all((hours_up, minutes_up)):
            msg = f"**{hours_up}** час. **{minutes_up}** мин. **{time_up}** сек. назад"
        elif minutes_up != 0:
            msg = f"**{minutes_up}** мин. **{time_up}** сек. назад"
        else:
            msg = f"**{time_up}** сек. назад"

        if is_windows:
            os_info = platform.uname()
            os_version = f'{os_info.system} {os_info.release}'
        elif is_mac:
            os_info = platform.mac_ver()
            os_version = f'Mac OS X {os_info[0]} {os_info[2]}'
        else:
            os_info = distro.linux_distribution()
            os_version = f'{os_info[0]} {os_info[1]}'

        emb = discord.Embed(title = 'Потребление ресурсов', color = colors['help'])
        emb.add_field(name = '<:cpu:868488839671476314>CPU', value = f'⠀⠀{ps.cpu_percent()}%', inline = True)
        emb.add_field(name = '<:ram:868489182383845376>RAM', value = f'⠀⠀{mem_used}/{mem_total}', inline = True)
        emb.add_field(name = '<:ping:868489884023787580>PING', value = f'⠀⠀{ping * 1000:.0f}ms\n', inline = True)
        emb.add_field(name = '<:os:868494322415312926>OS:', value = f'⠀⠀{os_version}', inline = True)
        emb.add_field(name = '<:start:868490519410511902>LAUNCH:', value = f'⠀⠀{msg}', inline = True)
        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = avatar(self.bot.user))
        emb.set_thumbnail(url = avatar(self.bot.user))
        await ctx.send(embed = emb)
        logger.info(f'Информация о загруженности бота - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Resource(bot))