import discord
import time

from datetime import datetime
from discord.ext import commands

from core.bot import avatar, is_owner
from core.embeds import Errors, Helpers
from core.logger import logger
from data.colors import colors
from scripts.parsers.steamid import parse_steamid
from scripts.parsers.imgs import imgs
from scripts.parsers.settings import settings
from scripts.parsers.emojis import emojis
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

    emoji = emojis['csgo_privillege']

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
            logger.debug('Пытаюсь подключиться к БД — Запросил пользователь: SYSTEM.')
            db = open_csgo_db_connection() # Открываем соединение с БД
            logger.debug('Подключение к БД установлено — Запросил пользователь: SYSTEM.')
            cursor = db.cursor() # Создаем курсор управления БД
            logger.debug('Курсор управления БД создан — Запросил пользователь: SYSTEM.')

            logger.debug('Пытаюсь отправить SQL запрос на получение данных из БД — Запросил пользователь: SYSTEM.')
            cursor.execute(f'SELECT * FROM vip_users WHERE account_id={steamid}') # Отправляем SQL запрос
            logger.debug('Данные из БД были получены — Запросил пользователь: SYSTEM.')
            result = cursor.fetchone() # Получаем первую строку из полученного кортежа
            logger.debug('Получена первая строка из полученного кортежа — Запросил пользователь: SYSTEM.')

            cursor.close()
            logger.debug('Доступ к курсору был закрыт — Запросил пользователь: SYSTEM.')
            db.close()
            logger.debug('Подключение к БД было закрыто — Запросил пользователь: SYSTEM.')
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
            logger.debug('Пытаюсь подключиться к БД — Запросил пользователь: SYSTEM.')
            db = open_csgo_db_connection() # Открываем соединение с БД
            logger.debug('Подключение к БД установлено — Запросил пользователь: SYSTEM.')
            cursor = db.cursor() # Создаем курсор управления БД
            logger.debug('Курсор управления БД создан — Запросил пользователь: SYSTEM.')

            logger.debug('Пытаюсь отправить SQL запрос на отправку данных в БД — Запросил пользователь: SYSTEM.')
            sql = ('INSERT INTO `vip_users` (`account_id`, `name`, `lastvisit`, `sid`, `group`, `expires`) VALUES (%s, %s, %s, %s, %s, %s)') 
            data = (int(steamid), username, int(lastvisit), 0, privillege, int(expiries))
            cursor.execute(sql, data) # Отправляем SQL запрос
            logger.debug('Данные были получены БД — Запросил пользователь: SYSTEM.')
            db.commit() # Сохраняем изменения в базе данных
            logger.debug('Изменения были сохранены в БД — Запросил пользователь: SYSTEM.')

            cursor.close()
            logger.debug('Доступ к курсору был закрыт — Запросил пользователь: SYSTEM.')
            db.close()
            logger.debug('Подключение к БД было закрыто — Запросил пользователь: SYSTEM.')
            return True
        except Exception as err:
            logger.error(err)
            return None

    def csgo_give_privillege_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}ксго\_выдать\_привилегию', value = 'Выдать привилегию на сервере CS:GO', inline = False)

    async def csgo_give_privillege_helper(self, ctx):
        emb = await Helpers.custom_image_embed(self, ctx, self.bot.user.avatar_url, 'server', 'Выдача привилегий CS:GO')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}ксго_выдать_привилегию <ссылка на стим> <привилегия из groups.ini> <Время в днях/часах>`\n┗ Выдаст игроку привилегию на определенный срок', inline = False)
        emb.add_field(name = 'Пример', value = f'`{settings["prefix"]}ксго_выдать_привилегию https://steamcommunity.com/id/ToilOfficial VIP 1d`\n┗ Выдаст игроку привилегию VIP на 1 день', inline = False)
        emb.add_field(name = 'Примечание', value = f'Время, на которое выдаётся привилегия, не может быть указано в месяцах/годах', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Выдаче привилегии у игрока в CS:GO" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    async def csgo_give_privillege_dtdb(self, ctx, steamid64, expiries, steamid3, nick, timestamp, privillege, result_timestamp):
        transfer_result = self.transfer_data_to_db(steamid3, nick, timestamp, privillege, result_timestamp)
        if transfer_result is True:
            emb = discord.Embed(title = f'Выдана привилегия на сервере CS:GO', color = colors['success'])
            emb.add_field(name = f'{self.emoji["steam_user"]} Ник', value = nick, inline = True)
            emb.add_field(name = f'{self.emoji["privillege"]} Привилегия', value = privillege, inline = True)
            emb.add_field(name = f'{self.emoji["expiries"]} Срок', value = expiries, inline = True)
            emb.add_field(name = f'{self.emoji["steam"]} Профиль в стиме', value= f'[Тык](https://steamcommunity.com/id/{steamid64})', inline = True)
            emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
            emb.set_author(name = datetime.now().strftime(settings['time_format']), icon_url = ctx.author.avatar_url)
            await ctx.send(embed = emb)
            logger.info(f'Выдана привилегия {privillege} (Срок: {expiries}) на сервере CS:GO игроку {nick} ("https://steamcommunity.com/id/{steamid64}") — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await Errors.custom_msg_embed(self, ctx, 'Не удалось отправить/сохранить данные в БД')
            logger.error(f'Не удалось отправить/сохранить данные о новой привилегии игрока на сервере CS:GO в БД — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

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
                    await self.csgo_give_privillege_dtdb(ctx, parser[0], expiries, steamid3, parser[-1], timestamp, privillege, result_timestamp)

                elif type(data_from_db) is tuple and data_from_db[0] == int(steamid3):
                    if int(data_from_db[5]) > int(timestamp):
                        emb = discord.Embed(title = f'У игрока уже есть привилегия на сервере CS:GO', color = colors['error'])
                        emb.set_author(name = 'Ошибка', icon_url = avatar(ctx.author))
                        emb.add_field(name = f'{self.emoji["steam_user"]} Ник', value = data_from_db[1], inline = True)
                        emb.add_field(name = f'{self.emoji["steam"]} SteamID3', value = data_from_db[0], inline = True)
                        emb.add_field(name = f'{self.emoji["start"]} Активность', value = f'<t:{data_from_db[2]}:D>\n<t:{data_from_db[2]}:R>', inline = True)
                        emb.add_field(name = f'{self.emoji["privillege"]} Привилегия', value = data_from_db[4], inline = True)
                        emb.add_field(name = f'{self.emoji["expiries"]} Срок', value = f'<t:{data_from_db[5]}:D>\n<t:{data_from_db[5]}:R>', inline = True)
                        emb.add_field(name = f'{self.emoji["steam"]} Профиль в стиме', value= f'[Тык](https://steamcommunity.com/id/{parser[0]})', inline = True)
                        emb.set_thumbnail(url = imgs['error'])
                        emb.set_footer(text = 'Aki © 2022 Все права защищены', icon_url = self.bot.user.avatar_url)
                        await ctx.send(embed = emb)
                        logger.info(f'У игрока {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}") уже есть привилегия {data_from_db[4]} (Срок: {data_from_db[5]}) на сервере CS:GO — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
                    else:
                        await self.csgo_give_privillege_dtdb(ctx, parser[0], expiries, steamid3, parser[-1], timestamp, privillege, result_timestamp)
                elif data_from_db is False:
                    await Errors.custom_msg_embed(self, ctx, 'Не удалось получить данные из БД')
                    logger.error(f'Не удалось получить данные из БД — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
                else:
                    await Errors.custom_msg_embed(self, ctx, 'Неизвестная ошибка')
                    logger.error(f'Произошла неизвестная ошибка — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            else:
                await Errors.custom_msg_embed(self, ctx, 'Произошла ошибка при парсинге стима игрока')
                logger.error(f'Не удалось получить подлинные данные о стиме игрока — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await Errors.no_permissions_embed(self, ctx)
            logger.warning(f'Неудачная попытка выдать привилегию на сервере CS:GO - Недостаточно прав — Запросил пользователь: {ctx.author} ({ctx.author.id}).')


    @csgo_give_privillege_command.error
    async def csgo_give_privillege_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await self.csgo_give_privillege_helper(ctx)
        else:
            await Errors.custom_msg_embed(self, ctx, error)
            logger.error('Ошибка "Не удалось выдать привилегию на сервере CS:GO" — Запросил пользователь: SYSTEM.')
            logger.error(error)

def setup(bot):
    bot.add_cog(CSGOGivePrivillege(bot))