import discord
import time

from datetime import datetime
from discord.ext import commands

from core.bot import avatar, is_owner
from core.logger import logger
from data.colors import colors
from scripts.parsers.steamid import parse_steamid
from scripts.parsers.imgs import imgs
from scripts.parsers.settings import settings
from scripts.database import open_csgo_db_connection

time_rotation = {
    's': '1',
    'm': '60',
    'h': '3600',
    'd': '86400',
    'w': '604800'
}


class CSGORemovePrivillege(commands.Cog):
    """Позволяет удалить привилегию игроку на серверах CS:GO"""

    def __init__(self, bot):
        self.bot = bot

    def get_data_from_db(self, steamid):
        """Получение данных из базы данных CS:GO

        Args:
            steamid: steamid3

        Returns:
            result: (848110702, 'Toil', 1639503546, 0, 'ADMIN', 0) - Success
            result: False - Fail
        """
        try:
            logger.debug('Пытаюсь подключиться к БД - Пользователь: SYSTEM.')
            db = open_csgo_db_connection() # Открываем соединение с БД
            logger.debug('Подключение к БД установлено - Пользователь: SYSTEM.')
            cursor = db.cursor() # Создаем курсор управления БД
            logger.debug('Курсор управления БД создан - Пользователь: SYSTEM.')

            logger.debug('Пытаюсь отправить SQL запрос на получение данных из БД - Пользователь: SYSTEM.')
            cursor.execute(f'SELECT * FROM vip_users WHERE account_id={steamid}') # Отправляем SQL запрос
            logger.debug('Данные из БД были получены - Пользователь: SYSTEM.')
            result = cursor.fetchone() # Получаем первую строку из полученного кортежа
            logger.debug('Получена первая строка из полученного кортежа - Пользователь: SYSTEM.')

            cursor.close()
            logger.debug('Доступ к курсору был закрыт - Пользователь: SYSTEM.')
            db.close()
            logger.debug('Подключение к БД было закрыто - Пользователь: SYSTEM.')
            return result
        except Exception as err:
            logger.error(err)
            return False

    def delete_data_to_db(self, steamid):
        """Удаление данных из базы данных CS:GO

        Args:
            steamid: steamid3

        Returns:
            result: True - Success
            result: None - Fail
        """
        try:
            logger.debug('Пытаюсь подключиться к БД - Пользователь: SYSTEM.')
            db = open_csgo_db_connection() # Открываем соединение с БД
            logger.debug('Подключение к БД установлено - Пользователь: SYSTEM.')
            cursor = db.cursor() # Создаем курсор управления БД
            logger.debug('Курсор управления БД создан - Пользователь: SYSTEM.')

            logger.debug('Пытаюсь отправить SQL запрос на удаление данных из БД - Пользователь: SYSTEM.')
            cursor.execute(f'DELETE FROM vip_users WHERE account_id={int(steamid)}') # Отправляем SQL запрос
            logger.debug('Данные были удалены из БД - Пользователь: SYSTEM.')
            db.commit() # Сохраняем изменения в базе данных
            logger.debug('Изменения были сохранены в БД - Пользователь: SYSTEM.')

            cursor.close()
            logger.debug('Доступ к курсору был закрыт - Пользователь: SYSTEM.')
            db.close()
            logger.debug('Подключение к БД было закрыто - Пользователь: SYSTEM.')
            return True
        except Exception as err:
            logger.error(err)
            return None
    @commands.command(aliases = [
                                'csgo_remove_privillege', 'cs_remove_privillege',
                                'ксго_удалить_привилегию', 'кс_удалить_привилегию',
                                ])
    async def csgo_remove_privillege_command(self, ctx, steam_link: str):
        """Удаление привилегии на сервере CS:GO

        Args:
            steamlink (str): Ссылка на профиль в стиме

        Returns:
            Embed - success
        """
        if is_owner(ctx.author.id) is True:
            try:
                parser = parse_steamid(steam_link)
            except Exception as err:
                parser = None
                logger.error('Произошла ошибка при парсинге. Возможно вы ввели несуществующий профиль')
                logger.error(err)
            logger.debug(f'Информация из парсера steamid: {parser}')
            if isinstance(parser, list):
                if parser[2].startswith('[U:1:'):
                    steamid3_1 = parser[2].split('[U:1:')
                    steamid3_2 = steamid3_1[1].split(']')
                    steamid3 = steamid3_2[0]

                data_from_db = self.get_data_from_db(steamid3)

                if type(data_from_db) is tuple and data_from_db[0] == int(steamid3):
                    delete_result = self.delete_data_to_db(steamid3)
                    if delete_result is True:
                        emb = discord.Embed(title = f'Удалена привилегия на сервере CS:GO', color = colors['success'])
                        emb.add_field(name='<:user:921910005094039563>Игрок', value = parser[-1], inline = True)
                        emb.add_field(name='<:privillege:921910024647872522>Привилегия', value = data_from_db[4], inline = True)
                        emb.add_field(name='<:expiries:921910297726451722>Срок', value = data_from_db[5], inline = True)
                        emb.add_field(name='<:steam:921909978850271284>Ссылка на профиль в стиме', value= f'https://steamcommunity.com/id/{parser[0]}', inline = False)
                        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                        emb.set_author(name = datetime.now().strftime(settings['time_format']), icon_url = ctx.author.avatar_url)
                        await ctx.send(embed = emb)
                        logger.info(f'У игрока {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}") удалена привилегия {data_from_db[4]} (Срок: {data_from_db[5]}) на сервере CS:GO - Пользователь: {ctx.author} ({ctx.author.id}).')
                    else:
                        emb = discord.Embed(title = f'Не удалось отправить/сохранить данные в БД', color = colors['error'])
                        emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                        emb.set_thumbnail(url = imgs['error'])
                        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                        await ctx.send(embed = emb)
                        logger.error(f'Не удалось отправить/сохранить данные в БД, о удалении привилегии у игрока на сервере CS:GO - Пользователь: {ctx.author} ({ctx.author.id}).')

                elif data_from_db is not tuple and data_from_db is not False:
                    emb = discord.Embed(title = f'У игрока нет привилегии на сервере CS:GO', color = colors['error'])
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.add_field(name='<:user:921910005094039563>Ник', value = parser[-1], inline = True)
                    emb.add_field(name='<:steam:921909978850271284>SteamID3', value = parser[2], inline = True)
                    emb.set_thumbnail(url = imgs['error'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                    await ctx.send(embed = emb)
                    logger.info(f'У игрока {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}") нет привилегии на сервере CS:GO - Пользователь: {ctx.author} ({ctx.author.id}).')

                elif data_from_db is False:
                    emb = discord.Embed(title = f'Не удалось получить данные из БД', color = colors['error'])
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                    await ctx.send(embed = emb)
                    logger.error(f'Не удалось получить данные из БД - Пользователь: {ctx.author} ({ctx.author.id}).')

                else:
                    emb = discord.Embed(title = f'Неизвестная ошибка', color = colors['error'])
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.set_thumbnail(url = imgs['error'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                    await ctx.send(embed = emb)
                    logger.error(f'Произошла неизвестная ошибка - Пользователь: {ctx.author} ({ctx.author.id}).')
            else:
                emb = discord.Embed(title = f'Не удалось спарсить данные о стиме игрока', color = colors['error'])
                emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                emb.set_thumbnail(url = imgs['error'])
                emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                await ctx.send(embed = emb)
                logger.info(f'Не удалось спарсить данные о стиме игрока - Пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await ctx.send(embed = discord.Embed(title = '`Вы не являетесь моим создателем!`', color = colors['error']))
            logger.warning(f'Неудачная попытка удалить привилегию на сервере CS:GO - Недостаточно прав - Пользователь: {ctx.author} ({ctx.author.id}).')

    @csgo_remove_privillege_command.error
    async def csgo_remove_privillege_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            emb = discord.Embed(title = 'Удаление привилегий CS:GO', color = colors['helper'])
            emb.set_author(name = 'Помощник', icon_url = avatar(ctx.author))
            emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}ксго_удалить_привилегию <ссылка на стим>`\n┗ Удалит привилегию игрока, если она существует', inline = False)
            emb.add_field(name = 'Пример', value = f'`{settings["prefix"]}ксго_удалить_привилегию https://steamcommunity.com/id/ToilOfficial`\n┗ Удалит привилегию у игрока', inline = False)
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            emb.set_thumbnail(url = imgs['server'])
            await ctx.send(embed = emb)
            logger.info(f'Выведена информация о "Удаление привилегии у игрока в CS:GO" - Пользователь: SYSTEM.')
        else:
            emb = discord.Embed(title = 'Ошибка удаления привилегии на сервере CS:G', color = colors['error'])
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            emb.add_field(name = 'Причина ошибки: ', value = error)
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            await ctx.send(embed = emb)
            logger.error('Ошибка удаления привилегии на сервере CS:GO - Пользователь: SYSTEM.')
            logger.error(error)
def setup(bot):
    bot.add_cog(CSGORemovePrivillege(bot))