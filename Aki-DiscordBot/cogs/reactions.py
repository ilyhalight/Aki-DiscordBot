import asyncio
import discord

from discord.ext import commands

from core.embeds import Errors, Helpers
from core.logger import logger
from scripts.parsers.settings import settings
from scripts.parsers.emojis import emojis

emoji_add = ["добавить", 'add']
emoji_del = ["удалить", "стереть", "очистить", 'remove', 'clear', 'delete', 'del']
emoji_clear = ["удалить_всё", "стереть_всё", "очистить_всё", "удалить_все", "стереть_все", "очистить_все", 'remove_all', 'clear_all', 'delete_all']


class Reactions(commands.Cog):
    """Взаимодействие с эмоджи"""

    emoji = emojis['reactions']


    def __init__(self, bot):
        self.bot = bot

    def reactions_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}реакция', value = 'Взаимодействие с реакциями', inline = False)

    async def reactions_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Реакции')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}реакция <действие> <id сообщения> <реакция>`\n┗ Взаимодействие с реакциями', inline = False)
        emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}реакция добавить 824428281104564264 {self.emoji["any"]}`\n┗ Добавит к сообщению с заданным айди реакцию {self.emoji["any"]}.', inline = False)
        emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}реакция очистить 824428281104564264 {self.emoji["any"]}`\n┗ Очистит в сообщение с заданным айди реакцию {self.emoji["any"]}.', inline = False)
        emb.add_field(name = 'Пример 3', value = f'`{settings["prefix"]}реакция очистить_все 824428281104564264`\n┗ Очистит в сообщение с заданным айди абсолютно все реакции.', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "реакция" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'emoji', 'reaction', 'react',
                                'эмодзи', 'эмоджи', 'реакция', 'реакт'
                                ])
    @commands.has_permissions(administrator = True)
    async def reactions_command(self, ctx, act: str = None, id: int = None, reaction: str = None):
        if all((act, id)):
            message = await ctx.message.channel.fetch_message(id)
            if act.lower() in emoji_add and reaction is not None:
                await message.add_reaction(reaction)
                logger.success(f'К сообщению "{message.id}" была добавлена реакция "{reaction}" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
                await ctx.message.add_reaction('✅')
            elif act.lower() in emoji_del and reaction is not None:
                await message.clear_reaction(reaction)
                logger.success(f'В сообщение "{message.id}" были очищены реакции "{reaction}" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
                await ctx.message.add_reaction('✅')
            elif act.lower() in emoji_clear:
                await message.clear_reactions()
                logger.success(f'В сообщение "{message.id}" были очищены все реакции — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
                await ctx.message.add_reaction('✅')
            else:
                await ctx.message.add_reaction('❌')
            await asyncio.sleep(5)
            await ctx.message.delete()
        else:
            await self.reactions_helper(ctx)

    @reactions_command.error
    async def reactions_command_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await self.reactions_helper(ctx)
        elif isinstance(error, commands.errors.CommandInvokeError):
            if error.args[0] == 'Command raised an exception: HTTPException: 400 Bad Request (error code: 10014): Unknown Emoji':
                await Errors.custom_msg_embed(self, ctx, 'Не удалось найти этот эмодзи в нашей базе')
            elif error.args[0] == 'Command raised an exception: NotFound: 404 Not Found (error code: 10008): Unknown Message':
                await Errors.custom_msg_embed(self, ctx, 'Сообщение с этим ID не найдено на этом сервере')
            else:
                await Errors.custom_msg_embed(self, ctx, error)
            logger.error(f'Не удалось произвести действие с реакциями - Причина: {error} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await Errors.custom_msg_embed(self, ctx, error)
            logger.error(f'Не удалось произвести действие с реакциями - Причина: {error} — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Reactions(bot))