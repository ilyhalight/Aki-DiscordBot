import discord
import asyncio
import random

from discord.ext import commands
from loguru import logger
from core.embeds import Errors, Helpers
from scripts.parsers.settings import settings

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


class Giveaway(commands.Cog):
    """Создание розыгрышей/конкурсов"""

    def __init__(self, bot):
        self.bot = bot

    def giveaway_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}розыгрыш', value = 'Создать розыгрыш', inline = False)

    async def giveaway_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Розыгрыши')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}розыгрыш <кол-во победителей> <время> <тест>`\n┗ Создаст розыгрыш от вашего лица на определенное время.', inline = False)
        emb.add_field(name = 'Пример', value = f'`{settings["prefix"]}розыгрыш 1 1d 1 Место: 1000 рублей`\n┗ Создаст розыгрыш на 1 день для 1 победителя', inline = False)
        emb.add_field(name = 'Примечание', value = f'Время розыгрыша не может бысть указано в месяцах/годах', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "Создании розыгрыша" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = ['giveaway', 'розыгрыш'])
    @commands.has_permissions(administrator = True)
    async def giveaway_command(self, ctx, winners = None, giveaway_time = None, *, text):
        counter = 0
        time_rotation = {
            's': '1',
            'm': '60',
            'h': '3600',
            'd': '86400',
            'w': '604800'
        }
        winners_text = 'Победители'
        top_places = ''
        alternative_time = ''
        if int(winners) > 0 and all((giveaway_time, text)): # Если победителей > 0, есть время и есть текст
            for s in giveaway_time: # Раскладываем переменную giveaway_time на буквы
                if s.lower() in time_rotation: # Проверяем есть ли в переменной giveaway_time буква совпадающающая со словарём time_rotation
                    intermediate_time = time_rotation[s.lower()] # Если такая буква есть, заносим её в новую переменную
                else:
                    alternative_time += f'{s}'
            if int(alternative_time) <= 0:
                alternative_time = 1
            final_time = int(alternative_time) * int(intermediate_time)
            end_time_str = display_time(final_time, 5)
            emb = discord.Embed(title = "🎉Розыгрыш начался🎉", description = f"**Внимание розыгрыш!\n\n{text}\n\nНажмите на реакцию ниже, чтобы принять участие**\nСпасибо <@{ctx.message.author.id}> за розыгрыш")
            emb.set_footer(text = f"{winners_text}: {winners} | Конец через {end_time_str}")
            message = await ctx.send(embed = emb)
            await message.add_reaction('🎫') # Добавляем емодзи
            logger.info(f'Розыгрыш начался — Запросил пользователь: {ctx.author} ({ctx.author.id})')
            await asyncio.sleep(final_time) # Асинхронное ожидание в секундах
            mess = await ctx.channel.fetch_message(message.id)
            winner_array = []
            for reaction in mess.reactions:
                if reaction.emoji == '🎫':
                    users = await reaction.users().flatten()
            if len(users) > 1:
                users.pop(0)
            while len(winner_array) < int(winners):
                winner = random.choice(users)
                if len(winner_array) >= len(users):
                    winner_array.append('Не удалось найти участника')
                elif winner in winner_array:
                    winner = random.choice(users)
                else:
                    winner_array.append(winner)
            while counter < int(winners):
                top_places += f'{counter + 1}) {winner_array[counter]}\n'
                counter += 1
            emb_final = discord.Embed(title = "🎉Розыгрыш закончился🎉", description = f"**Внимание розыгрыш закончился!\n\n{text}\n\nПобедители:\n{top_places}**\nСпасибо <@{ctx.message.author.id}> за розыгрыш")
            emb_final.set_footer(text = f"{winners_text}: {winners} | Закончился")

            await message.edit(embed = emb_final)
            logger.info(f'Розыгрыш закончился — Запросил пользователь: {ctx.author} ({ctx.author.id})')


    @giveaway_command.error
    async def giveaway_command_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            await self.giveaway_helper(ctx)
            logger.error(f'Не удалось создать розыгрыш - Причина: Недостаточно аргументов — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            logger.error(error)
        else:
            await Errors.custom_msg_embed(self, ctx, error)
            logger.error('Ошибка создания розыгрыша — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            logger.error(error)

def setup(bot):
    bot.add_cog(Giveaway(bot))