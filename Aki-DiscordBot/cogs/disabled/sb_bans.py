# from typing import final
# import discord
# import time

# from datetime import datetime
# from discord.ext import commands

# from core.bot import avatar, is_owner
# from core.logger import logger
# from data.colors import colors
# from scripts.parsers.steamid import parse_steamid
# from scripts.parsers.imgs import imgs
# from scripts.parsers.settings import settings
# from scripts.database import open_sb_db_connection

# time_rotation = {
#     's': '1',
#     'm': '60',
#     'h': '3600',
#     'd': '86400',
#     'w': '604800'
# }

# def get_data_from_db(steamid):
#     """Получение данных из базы данных CS:GO

#     Args:
#         steamid: steamID

#     Returns:
#         result: (3, '0.0.0.0', 'STEAM_0:0:613177694', 1639503546, 1639503546, 0, 'Читы', 0, '0.0.0.0', 'RU', Null, Null, Null, 0, Null)
#     """
#     logger.debug('Пытаюсь подключиться к БД - Пользователь: SYSTEM.')
#     db = open_sb_db_connection() # Открываем соединение с БД
#     logger.debug('Подключение к БД установлено - Пользователь: SYSTEM.')
#     cursor = db.cursor(buffered = True) # Создаем курсор управления БД
#     logger.debug('Курсор управления БД создан - Пользователь: SYSTEM.')

#     logger.debug('Пытаюсь отправить SQL запрос на получение данных из БД - Пользователь: SYSTEM.')
#     cursor.execute(f'SELECT * FROM sb_bans WHERE authid="{steamid}"') # Отправляем SQL запрос
#     logger.debug('Данные из БД были получены - Пользователь: SYSTEM.')
#     result = cursor.fetchone() # Получаем первую строку из полученного кортежа
#     logger.debug('Пытаюсь закрыть доступ к курсору БД - Пользователь: SYSTEM.')
#     cursor.close()
#     logger.debug('Пытаюсь закрыть доступ к БД - Пользователь: SYSTEM.')
#     db.close()
#     logger.debug('Подключение к БД было закрыто - Пользователь: SYSTEM.')
#     return result


# def transfer_data_to_db(steamid, username, current_time, end_time, lenght, reason):
#     """Передача данных в базу данных CS:GO"""
#     try:
#         logger.debug('Пытаюсь подключиться к БД - Пользователь: SYSTEM.')
#         db = open_sb_db_connection() # Открываем соединение с БД
#         logger.debug('Подключение к БД установлено - Пользователь: SYSTEM.')
#         cursor = db.cursor(buffered = True) # Создаем курсор управления БД
#         logger.debug('Курсор управления БД создан - Пользователь: SYSTEM.')

#         logger.debug('Пытаюсь отправить SQL запрос на отправку данных в БД - Пользователь: SYSTEM.')
#         sql = ('INSERT INTO `sb_bans` (`bid`, `ip`, `authid`, `name`, `created`, `ends`, `length`, `reason`, `aid`, `adminIp`, `sid`, `country`, `RemovedBy`, `RemoveType`, `RemovedOn`, `type`, `ureason`) VALUES (NULL, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL, NULL, NULL, %s, NULL)')
#         data = (steamid, username, current_time, end_time, lenght, reason, 0, '0.0.0.0', 0, 0)
#         cursor.execute(sql, data) # Отправляем SQL запрос
#         logger.debug('Данные были получены БД - Пользователь: SYSTEM.')
#         db.commit() # Сохраняем изменения в базе данных
#         logger.debug('Пытаюсь закрыть доступ к курсору БД - Пользователь: SYSTEM.')
#         cursor.close()
#         logger.debug('Пытаюсь закрыть доступ к БД - Пользователь: SYSTEM.')
#         db.close()
#         logger.debug('Подключение к БД было закрыто - Пользователь: SYSTEM.')
#         return True
#     except Exception as err:
#         logger.error(err)
#         return None

# def update_data_to_db(steamid, end_time, lenght):
#     """Передача данных в базу данных CS:GO"""
#     try:
#         logger.debug('Пытаюсь подключиться к БД - Пользователь: SYSTEM.')
#         db = open_sb_db_connection() # Открываем соединение с БД
#         logger.debug('Подключение к БД установлено - Пользователь: SYSTEM.')
#         cursor = db.cursor(buffered = True) # Создаем курсор управления БД
#         logger.debug('Курсор управления БД создан - Пользователь: SYSTEM.')

#         logger.debug('Пытаюсь отправить SQL запрос на обновление данных из БД - Пользователь: SYSTEM.')
#         sql = (f'UPDATE `sb_bans` SET `ends`=%s, `length`=%s, `RemoveType`=NULL, `RemovedOn`=NULL WHERE authid="{steamid}"')
#         data = (end_time, lenght)
#         cursor.execute(sql, data) # Отправляем SQL запрос
#         logger.debug('Данные в БД были обновлены - Пользователь: SYSTEM.')
#         db.commit() # Сохраняем изменения в базе данных
#         logger.debug('Пытаюсь закрыть доступ к курсору БД - Пользователь: SYSTEM.')
#         cursor.close()
#         logger.debug('Пытаюсь закрыть доступ к БД - Пользователь: SYSTEM.')
#         db.close()
#         logger.debug('Подключение к БД было закрыто - Пользователь: SYSTEM.')
#         return True
#     except Exception as err:
#         logger.error(err)
#         return None


# class SB_bans(commands.Cog):
#     """Выдать бан в SourceBans"""

#     def __init__(self, bot):
#         self.bot = bot

#     def sb_ban_help(self, prefix, emb: discord.Embed):
#         return emb.add_field(name = f'{prefix}сб_бан', value = 'Выдать бан в SourceBans', inline = False)

#     @commands.command(aliases = [
#                                 'sb_ban', 'sourceban_ban', 'sourcebans_ban',
#                                 'сб_бан', 'соурсбан_бан', 'соурсбанс_бан'
#                                 ])
#     async def sb_ban_command(self, ctx, steam_link: str, expiries: str, *, reason):
#         if is_owner(ctx.author.id) is True:
#             # Парсим steamID
#             parser = parse_steamid(steam_link)
#             logger.debug(f'Информация из парсера steamid: {parser}')
#             if parser != None or parser != []:
#                 if parser[1].startswith('STEAM_'):
#                     steamid = parser[1]
#                     steamid_new = steamid[7:]
#                     steamid_array = ['STEAM_0'+steamid_new, 'STEAM_1'+steamid_new]
#                     print(steamid_array)

#                 # Преобразуем время в unix
#                 alternative_time = ''

#                 for s in expiries:
#                     if s.lower() in time_rotation:
#                         intermediate_time = time_rotation[s.lower()]
#                     else:
#                         alternative_time += f'{s}'

#                 if int(alternative_time) <= 0:
#                     alternative_time = 1

#                 final_time = int(alternative_time) * int(intermediate_time)
#                 timestamp = int(time.time())
#                 result_timestamp = int(timestamp) + int(final_time)
#                 if int(final_time) > 86400000:
#                     result_timestamp = int(timestamp)
#                     final_time = 0
#                 data_from_db = get_data_from_db(steamid_array[0])
#                 print(data_from_db)
#                 data_from_db2 = get_data_from_db(steamid_array[1])
#                 print(data_from_db2)

#                 if data_from_db is not None and type(data_from_db) == tuple and data_from_db[2] == steamid_array[0] or data_from_db2 is not None and type(data_from_db2) == tuple and data_from_db2[2] == steamid_array[1]:
#                     if data_from_db is not None:
#                         embed_data = data_from_db
#                     else:
#                         embed_data = data_from_db2

#                     if embed_data[13] == 'U' or embed_data[13] == 'E':
#                         updated_info = update_data_to_db(steamid, result_timestamp, final_time)
#                         if updated_info is True:
#                             emb = discord.Embed(title = f'Бан игрока {embed_data[3]} в Sourcebans был обновлен', color = colors['error'])
#                             emb.add_field(name='<:user:921910005094039563>Ник', value = embed_data[3], inline = True)
#                             emb.add_field(name='<:steam:921909978850271284>SteamID', value = embed_data[2], inline = True)
#                             emb.add_field(name='<:start:868490519410511902>Начало', value = datetime.utcfromtimestamp(timestamp), inline = True)
#                             emb.add_field(name='<:start:868490519410511902>Окончание', value = datetime.utcfromtimestamp(result_timestamp), inline = True)
#                             emb.add_field(name='<:start:868490519410511902>Срок', value = expiries, inline = True)
#                             emb.add_field(name='<:expiries:921910297726451722>Причина', value = reason, inline = True)
#                             emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
#                             emb.set_thumbnail(url = imgs['error'])
#                             emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
#                             await ctx.send(embed = emb)
#                             logger.info(f'Бан игрока {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}") в системе SourceBans (Срок: {embed_data[6]}) был обновлён - Пользователь: {ctx.author} ({ctx.author.id}).')
#                         else:
#                             emb = discord.Embed(title = f'У игрока уже есть бан в системе Sourcebans', color = colors['error'])
#                             emb.add_field(name='<:user:921910005094039563>Ник', value = embed_data[3], inline = True)
#                             emb.add_field(name='<:steam:921909978850271284>SteamID', value = embed_data[2], inline = True)
#                             emb.add_field(name='<:start:868490519410511902>Начало', value = datetime.utcfromtimestamp(embed_data[4]), inline = True)
#                             emb.add_field(name='<:start:868490519410511902>Окончание', value = datetime.utcfromtimestamp(embed_data[5]), inline = True)
#                             emb.add_field(name='<:start:868490519410511902>Срок', value = datetime.utcfromtimestamp(embed_data[6]), inline = True)
#                             emb.add_field(name='<:expiries:921910297726451722>Причина', value = embed_data[7], inline = True)
#                             emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
#                             emb.set_thumbnail(url = imgs['error'])
#                             emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
#                             await ctx.send(embed = emb)
#                             logger.info(f'У игрока {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}") уже есть действующий бан (Срок: {embed_data[6]}) в системе SourceBans - Пользователь: {ctx.author} ({ctx.author.id}).')
#                     else:
#                         emb = discord.Embed(title = f'У игрока уже есть бан в системе Sourcebans', color = colors['error'])
#                         emb.add_field(name='<:user:921910005094039563>Ник', value = embed_data[3], inline = True)
#                         emb.add_field(name='<:steam:921909978850271284>SteamID', value = embed_data[2], inline = True)
#                         emb.add_field(name='<:start:868490519410511902>Начало', value = datetime.utcfromtimestamp(embed_data[4]), inline = True)
#                         emb.add_field(name='<:start:868490519410511902>Окончание', value = datetime.utcfromtimestamp(embed_data[5]), inline = True)
#                         emb.add_field(name='<:start:868490519410511902>Срок', value = datetime.utcfromtimestamp(embed_data[6]), inline = True)
#                         emb.add_field(name='<:expiries:921910297726451722>Причина', value = embed_data[7], inline = True)
#                         emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
#                         emb.set_thumbnail(url = imgs['error'])
#                         emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
#                         await ctx.send(embed = emb)
#                         logger.info(f'У игрока {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}") уже есть действующий бан (Срок: {embed_data[6]}) в системе SourceBans - Пользователь: {ctx.author} ({ctx.author.id}).')

#                 # if data_from_db is None
#                 elif type(data_from_db) != tuple and type(data_from_db2) != tuple:
#                     transfer_result = transfer_data_to_db(steamid_array[0], parser[-1], timestamp, result_timestamp, final_time, reason)
#                     if transfer_result is True:
#                         emb = discord.Embed(title = f'Выдан новый бан в SourceBans', color = colors['success'])
#                         emb.add_field(name='<:user:921910005094039563>Игрок', value = parser[-1], inline = True)
#                         emb.add_field(name='<:expiries:921910297726451722>Срок', value = expiries, inline = True)
#                         emb.add_field(name='<:steam:921909978850271284>Ссылка на профиль в стиме', value= f'https://steamcommunity.com/id/{parser[0]}', inline = False)
#                         emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
#                         emb.set_author(name = datetime.now().strftime(settings['time_format']), icon_url = ctx.author.avatar_url)
#                         await ctx.send(embed = emb)
#                         logger.info(f'Выдан новый бан в системе SourceBans (Срок: {expiries}), игрок {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}")  - Пользователь: {ctx.author} ({ctx.author.id}).')
#                     else:
#                         emb = discord.Embed(title = f'Не удалось отправить/сохранить данные в БД', color = colors['error'])
#                         emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
#                         emb.set_thumbnail(url = imgs['error'])
#                         emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
#                         await ctx.send(embed = emb)
#                         logger.info(f'Не удалось отправить/сохранить данные о новом бане игрока SourceBans в БД  - Пользователь: {ctx.author} ({ctx.author.id}).')

#                 else:
#                     await ctx.send('Произошла неизвестная ошибка')
#             else:
#                 await ctx.send('Произошла ошибка. Не удалось получить информацию из парсера')
#         else:
#             await ctx.send(embed = discord.Embed(title = '`Вы не являетесь моим создателем!`', color = colors['error']))
#             logger.warning(f'Попытка выдать привилегию на сервере CS:GO - Пользователь: {ctx.author} ({ctx.author.id}).')

#     @sb_ban_command.error
#     async def sb_ban_command_error(self, ctx, error):
#         if isinstance(error, commands.errors.MissingRequiredArgument):
#             emb = discord.Embed(title = 'Помощник - Выдать бан в SourceBans', color = colors['helper'])
#             emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}sb_ban <ссылка на стим> <Время в днях/часах> [Причина]`\n┗ Выдаст игроку бан на определенный срок', inline = False)
#             emb.add_field(name = 'Пример', value = f'`{settings["prefix"]}sb_ban https://steamcommunity.com/id/ToilOfficial 1d Читы`\n┗ Выдаст игроку бан на 1 день с причиной "Читы"', inline = False)
#             emb.add_field(name = 'Примечание', value = f'Время бана не может быть указано в месяцах/годах', inline = False)
#             emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
#             emb.set_thumbnail(url = imgs['server'])
#             await ctx.send(embed = emb)
#         else:
#             emb = discord.Embed(title = 'Ошибка', description = 'Ошибка выдачи привилегии на сервере CS:GO', color = colors['error'])
#             emb.add_field(name = 'Причина ошибки: ', value = error)
#             emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
#             await ctx.send(embed = emb)
#             logger.warning('Ошибка выдачи привилегии на сервере CS:GO.')
#             logger.error(error)
# def setup(bot):
#     bot.add_cog(SB_bans(bot))