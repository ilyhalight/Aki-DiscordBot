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


class CSGOGivePrivillege(commands.Cog):
    """Позволяет выдать привилегию игроку на серверах CS:GO """

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

    def transfer_data_to_db(self, steamid, username, lastvisit, privillege, expiries):
        """Передача данных в базу данных CS:GO

        Args:
            steamid (int): steamid3 без [], :
            username (str): Имя игрока
            lastvisit (int): Последний вход на сервер (можно указать любую дату, главное в unix формате)
            privillege (str): Название привилегии, как записано в groups.ini
            expiries (int): Дата истечения привилегии (unix формат)

        Returns:
            result: True - Успех
            result: None - Неудача
        """
        try:
            logger.debug('Пытаюсь подключиться к БД - Пользователь: SYSTEM.')
            db = open_csgo_db_connection() # Открываем соединение с БД
            logger.debug('Подключение к БД установлено - Пользователь: SYSTEM.')
            cursor = db.cursor() # Создаем курсор управления БД
            logger.debug('Курсор управления БД создан - Пользователь: SYSTEM.')

            logger.debug('Пытаюсь отправить SQL запрос на отправку данных в БД - Пользователь: SYSTEM.')
            sql = ('INSERT INTO `vip_users` (`account_id`, `name`, `lastvisit`, `sid`, `group`, `expires`) VALUES (%s, %s, %s, %s, %s, %s)') 
            data = (int(steamid), username, int(lastvisit), 0, privillege, int(expiries))
            cursor.execute(sql, data) # Отправляем SQL запрос
            logger.debug('Данные были получены БД - Пользователь: SYSTEM.')
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
                                'csgo_give_privillege', 'cs_give_privillege',
                                'ксго_выдать_привилегию', 'кс_выдать_привилегию',
                                ])
    async def csgo_give_privillege_command(self, ctx, steam_link: str, privillege: str, expiries: str):
        """Выдача привилегии на сервере CS:GO

        Args:
            steamlink (str): Ссылка на профиль в стиме
            privillege (str): Название привилегии, как записано в groups.ini
            expiries (str): На какое время выдавать, не ставьте слишком огромное количество (желательно не более 9999 дней)

        Returns:
            Embed-message
        """
        if is_owner(ctx.author.id) is True:
            try:
                parser = parse_steamid(steam_link) # Парсим steamID
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

                # Преобразуем время в unix
                alternative_time = ''

                for s in expiries:
                    if s.lower() in time_rotation:
                        intermediate_time = time_rotation[s.lower()]
                    else:
                        alternative_time += f'{s}'

                if int(alternative_time) <= 0:
                    alternative_time = 1

                final_time = int(alternative_time) * int(intermediate_time)
                timestamp = int(time.time())
                result_timestamp = int(timestamp) + int(final_time)
                data_from_db = self.get_data_from_db(steamid3)

                if type(data_from_db) is not tuple and data_from_db is not False:
                    transfer_result = self.transfer_data_to_db(steamid3, parser[-1], timestamp, privillege, result_timestamp)
                    if transfer_result is True:
                        emb = discord.Embed(title = f'Выдана привилегия на сервере CS:GO', color = colors['success'])
                        emb.add_field(name='<:user:921910005094039563>Игрок', value = parser[-1], inline = True)
                        emb.add_field(name='<:privillege:921910024647872522>Привилегия', value = privillege, inline = True)
                        emb.add_field(name='<:expiries:921910297726451722>Срок', value = expiries, inline = True)
                        emb.add_field(name='<:steam:921909978850271284>Ссылка на профиль в стиме', value= f'https://steamcommunity.com/id/{parser[0]}', inline = False)
                        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                        emb.set_author(name = datetime.now().strftime(settings['time_format']), icon_url = ctx.author.avatar_url)
                        await ctx.send(embed = emb)
                        logger.info(f'Выдана привилегия {privillege} (Срок: {expiries}) на сервере CS:GO игроку {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}") - Пользователь: {ctx.author} ({ctx.author.id}).')
                    else:
                        emb = discord.Embed(title = f'Не удалось отправить/сохранить данные в БД', color = colors['error'])
                        emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                        emb.set_thumbnail(url = imgs['error'])
                        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                        await ctx.send(embed = emb)
                        logger.error(f'Не удалось отправить/сохранить данные о новой привилегии игрока на сервере CS:GO в БД - Пользователь: {ctx.author} ({ctx.author.id}).')

                elif type(data_from_db) is tuple and data_from_db[0] == int(steamid3):
                    emb = discord.Embed(title = f'У игрока уже есть привилегия на сервере CS:GO', color = colors['error'])
                    emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                    emb.add_field(name='<:user:921910005094039563>Ник', value = data_from_db[1], inline = True)
                    emb.add_field(name='<:steam:921909978850271284>SteamID3', value = data_from_db[0], inline = True)
                    emb.add_field(name='<:start:868490519410511902>Активность', value = datetime.utcfromtimestamp(data_from_db[2]), inline = True)
                    emb.add_field(name='<:privillege:921910024647872522>Привилегия', value = data_from_db[4], inline = True)
                    emb.add_field(name='<:expiries:921910297726451722>Срок', value = data_from_db[5], inline = True)
                    emb.set_thumbnail(url = imgs['error'])
                    emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                    await ctx.send(embed = emb)
                    logger.info(f'У игрока {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}") уже есть привилегия {data_from_db[4]} (Срок: {data_from_db[5]}) на сервере CS:GO - Пользователь: {ctx.author} ({ctx.author.id}).')

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
                emb = discord.Embed(title = f'Произошла ошибка при парсинге стима игрока', color = colors['error'])
                emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                emb.set_thumbnail(url = imgs['error'])
                emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                await ctx.send(embed = emb)
                logger.error(f'Не удалось получить подлинные данные о стиме игрока - Пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await ctx.send(embed = discord.Embed(title = '`Вы не являетесь моим создателем!`', color = colors['error']))
            logger.warning(f'Неудачная попытка выдать привилегию на сервере CS:GO - Недостаточно прав - Пользователь: {ctx.author} ({ctx.author.id}).')

    @csgo_give_privillege_command.error
    async def csgo_give_privillege_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            emb = discord.Embed(title = 'Выдача привилегий CS:GO', color = colors['helper'])
            emb.set_author(name = 'Помощник', icon_url = avatar(ctx.author))
            emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}ксго_выдать_привилегию <ссылка на стим> <привилегия из groups.ini> <Время в днях/часах>`\n┗ Выдаст игроку привилегию на определенный срок', inline = False)
            emb.add_field(name = 'Пример', value = f'`{settings["prefix"]}ксго_выдать_привилегию https://steamcommunity.com/id/ToilOfficial VIP 1d`\n┗ Выдаст игроку привилегию VIP на 1 день', inline = False)
            emb.add_field(name = 'Примечание', value = f'Время, на которое выдаётся привилегия, не может быть указано в месяцах/годах', inline = False)
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            emb.set_thumbnail(url = imgs['server'])
            await ctx.send(embed = emb)
            logger.info(f'Выведена информация о "Выдаче привилегии у игрока в CS:GO" - Пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            emb = discord.Embed(title = 'Не удалось выдать привилегию на сервере CS:GO', color = colors['error'])
            emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
            emb.add_field(name = 'Причина ошибки: ', value = error)
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            await ctx.send(embed = emb)
            logger.error('Ошибка "Не удалось выдать привилегию на сервере CS:GO" - Пользователь: SYSTEM.')
            logger.error(error)
def setup(bot):
    bot.add_cog(CSGOGivePrivillege(bot))