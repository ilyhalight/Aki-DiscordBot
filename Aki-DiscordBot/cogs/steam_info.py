import discord
import os

from discord.ext import commands
from core.logger import logger
from core.embeds import Errors, Helpers
from data.colors import colors
from modules.api.steam import SteamApi
from scripts.env import get_env
from scripts.parsers.settings import settings
from scripts.parsers.emojis import emojis
from scripts.parsers.steam.get_steamid64 import get_steamid64

class SteamInfo(commands.Cog):
    """Показывает информацию о профиле стима"""

    emoji = emojis['steam']

    def __init__(self, bot):
        self.bot = bot

    def steaminfo_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}стим', value = 'Показать информацию о стим профиле', inline = False)

    async def steaminfo_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Информация о стим профиле')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}стим <ссылка на профиль или steamid64>`\n┗ Выведет информацию о стим профиле.', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Информация о стим профиле" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    # steam_id_url - ссылка на профиль или steamid64 профиля
    @commands.command(aliases = [
                                'steaminfo', 'steam_info', 'steam', 'steaminformation', 'steam_information',
                                'стиминфо', 'стим_инфо', 'стим', 'стиминформация', 'стим_информация'
                                ])
    async def steaminfo_command(self, ctx, steam_id_url: str):
        if (steam_id_url.startswith('https://steamcommunity.com') or steam_id_url.startswith('https://www.steamcommunity.com') or steam_id_url.startswith('steamcommunity.com') or steam_id_url[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']):
            if steam_id_url[0] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                if steam_id_url.startswith('steamcommunity.com'):
                    steam_id_url = 'https://' + steam_id_url
                steamid64 = get_steamid64(steam_id_url)
                if steamid64 is None:
                    await Errors.custom_msg_embed(self, ctx, 'Steamid64 - None. Проверьте правильность введенных аргументов')
                    return logger.error(f'Не удалось вывести информацию о стим профиле — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            else:
                steamid64 = steam_id_url
            get_env()
            steam_res = SteamApi.GetPlayerSummaries(os.environ.get('STEAM_WEB_APIKEY'), steamid64)\

            if steam_res['communityvisibilitystate'] == 1:
                profile_status = 'Приватный'
            else:
                profile_status = 'Открытый'

            if steam_res['personastate'] == 1:
                activity_status = 'Онлайн'
            elif steam_res['personastate'] == 2:
                activity_status = 'Занят'
            elif steam_res['personastate'] == 3:
                activity_status = 'Нет на месте'
            elif steam_res['personastate'] == 4:
                activity_status = 'Спит'
            elif steam_res['personastate'] == 5:
                activity_status = 'Ищет для обмена'
            elif steam_res['personastate'] == 6:
                activity_status = 'Ищет для игры'
            else:
                activity_status = 'Не в сети'

            try:
                if steam_res['lastlogoff'] is not None:
                    lastlog = steam_res['lastlogoff']
            except:
                lastlog = None

            try:
                if steam_res['realname'] is not None:
                    real_name = steam_res['realname']
            except:
                real_name = None

            try:
                if steam_res['loccountrycode'] is not None:
                    profile_cc = steam_res['loccountrycode']
            except:
                profile_cc = None

            try:
                if steam_res['gameextrainfo'] is not None:
                    game_info = steam_res['gameextrainfo']
            except:
                game_info = None

            emb = discord.Embed(title = f'Информация о стиме {steam_res["personaname"]}', colour = colors['help'])
            if real_name is not None:
                emb.add_field(name = f'{self.emoji["name"]} Имя', value = steam_res['realname'], inline = True)
            emb.add_field(name = f'{self.emoji["username"]} Ник', value = steam_res['personaname'], inline = True)
            emb.add_field(name = f'{self.emoji["profile"]} Статус профиля', value = profile_status, inline = True)
            if lastlog is not None and activity_status == 'Не в сети':
                emb.add_field(name = f'{self.emoji["target"]} Статус активности', value = f'{activity_status}\n<t:{lastlog}:R>', inline = True)
            else:
                emb.add_field(name = f'{self.emoji["target"]} Статус активности', value = activity_status, inline = True)
            if profile_cc is not None:
                emb.add_field(name = f'{self.emoji["country"]} Код страны', value = profile_cc, inline = True)
            if game_info is not None:
                emb.add_field(name = f'{self.emoji["playing"]} Играет в', value = game_info, inline = True)
            emb.add_field(name = f'{self.emoji["date"]} Дата создания', value = f'<t:{steam_res["timecreated"]}:D>\n<t:{steam_res["timecreated"]}:R>', inline = True)
            emb.add_field(name = f'{self.emoji["steam"]} Профиль в стиме', value = f'[Тык]({steam_res["profileurl"]})', inline = True)
            emb.set_author(name = f'Steamid64: {steam_res["steamid"]}')
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            emb.set_thumbnail(url = steam_res["avatarfull"])
            await ctx.send(embed = emb)
            logger.info(f'Выведена информация о стим профиле {steam_res["personaname"]} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await self.steaminfo_helper(ctx)

    @steaminfo_command.error
    async def steaminfo_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await self.steaminfo_helper(ctx)
            logger.error(f'Не удалось вывести информацию о стим профиле - Причина: {error} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            logger.error(error)
        else:
            await Errors.custom_msg_embed(self, ctx, error)
            logger.error(error)

def setup(bot):
    bot.add_cog(SteamInfo(bot))