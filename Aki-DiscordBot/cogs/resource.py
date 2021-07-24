import discord
import time
import psutil as ps

from discord.ext import commands

from misc.global_vars import *
from tools.parsing import lang
from tools.internal_utils import bytes2Human
from core.bot import user_avatar

start_time = time.time()

ping_list = [
            {
                'ping': 0.00000000000000000,
                'emoji': '🟩🔳🔳🔳🔳'
            },
            {
                'ping': 0.10000000000000000,
                'emoji': '🟧🟩🔳🔳🔳'
            },
            {
                'ping': 0.15000000000000000,
                'emoji': '🟥🟧🟩🔳🔳'
            },
            {
                'ping': 0.20000000000000000,
                'emoji': '🟥🟥🟧🟩🔳'
            },
            {
                'ping': 0.25000000000000000,
                'emoji': '🟥🟥🟥🟧🟩'
            },
            {
                'ping': 0.30000000000000000,
                'emoji': '🟥🟥🟥🟥🟧'
            },
            {
                'ping': 0.35000000000000000,
                'emoji': '🟥🟥🟥🟥🟥'
            }
]

class Resource(commands.Cog):
    """Shows system information about the bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['resources', 'resource', 'bot_resources', 'bot_resource', 'загруженность', 'загруженностьбота', 'загруженность_бота', 'ресурсыбота', 'ресурсы_бота'])
    async def resource_analytics_command(self, ctx):
        mem = ps.virtual_memory()
        ping = self.bot.ws.latency

        for ping_one in ping_list:
            if ping <= ping_one["ping"]:
                ping_emoji = ping_one["emoji"]
                break

        time_up = time.time() - start_time
        days_up = round(time_up) // 86400
        time_up %= 86400
        hours_up = round(time_up) // 3600
        time_up %= 3600
        minutes_up = round(time_up) // 60
        time_up = round(time_up % 60)
        msg = f"**{days_up}** дн. **{hours_up}** час. **{minutes_up}** мин. **{time_up}** сек. назад :alarm_clock: "

        emb = discord.Embed(title = 'Загрузка бота', color = COLOR['bot resource'])
        emb.add_field(name = 'Использование CPU', value = f'В настоящее время используется: {ps.cpu_percent()}%', inline = True)
        emb.add_field(name = 'Использование RAM', value = f'Доступно: {bytes2Human(mem.available, "system")}\n' f'Используется: {bytes2Human(mem.used, "system")} ({mem.percent}%)\n' f'Всего: {bytes2Human(mem.total, "system")}', inline = True)
        emb.add_field(name = 'Пинг Бота', value = f'Пинг: {ping * 1000:.0f}ms\n'f'`{ping_emoji}`', inline = True)
        emb.add_field(name = 'Бот запустился:', value = msg, inline = True)
        emb.set_footer(text = lang['copyright'], icon_url = user_avatar(self.bot.user))
        await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(Resource(bot))