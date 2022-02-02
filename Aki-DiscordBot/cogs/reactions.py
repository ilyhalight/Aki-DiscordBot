import discord

from discord.ext import commands

from core.embeds import Helpers
from core.logger import logger
from scripts.parsers.settings import settings
from scripts.parsers.emojis import emojis

emoji_add = ["добавить", 'add']
emoji_del = ["удалить", "стереть", "очистить", 'remove', 'clear', 'delete', 'del']
emoji_clear = ["удалить_всё", "стереть_всё", "очистить_всё", "удалить_все", "стереть_все", "очистить_все", 'remove_all', 'clear_all', 'delete_all']

emoji = emojis['reactions']

class Reactions(commands.Cog):
    """Взаимодействие с эмоджи"""

    def __init__(self, bot):
        self.bot = bot

    def reactions_help(self, prefix, emb: discord.Embed):
        return emb.add_field(name = f'{prefix}реакция', value = 'Взаимодействие с реакциями', inline = False)

    async def reactions_helper(self, ctx):
        emb = await Helpers.default_embed(self, ctx, self.bot.user.avatar_url, 'Реакции')
        emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}реакция <действие> <id сообщения> <реакция>`\n┗ Взаимодействие с реакциями', inline = False)
        emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}реакция добавить 824428281104564264 {emoji["any"]}`\n┗ Добавит к сообщению с заданным айди реакцию {emoji["any"]}.', inline = False)
        emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}реакция очистить 824428281104564264 {emoji["any"]}`\n┗ Очистит в сообщение с заданным айди реакцию {emoji["any"]}.', inline = False)
        emb.add_field(name = 'Пример 3', value = f'`{settings["prefix"]}реакция очистить_все 824428281104564264`\n┗ Очистит в сообщение с заданным айди абсолютно все реакции.', inline = False)
        await ctx.send(embed = emb)
        logger.info(f'Выведена информация о "реакция" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')

    @commands.command(aliases = [
                                'emoji', 'reaction', 'react',
                                'эмодзи', 'эмоджи', 'реакция', 'реакт'
                                ])
    @commands.has_permissions(administrator = True)
    async def reactions_command(self, ctx, act: str = None, id: int = None, reaction: str = None):
        if act is not None and id is not None:
            await ctx.message.delete()
            message = await ctx.message.channel.fetch_message(id)
            if act.lower() in emoji_add and reaction is not None:
                await message.add_reaction(reaction)
                logger.success(f'К сообщению "{message.id}" была добавлена реакция "{reaction}" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            if act.lower() in emoji_del and reaction != None:
                await message.clear_reaction(reaction)
                logger.success(f'В сообщение "{message.id}" были очищены реакции "{reaction}" — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
            if act.lower() in emoji_clear:
                await message.clear_reactions()
                logger.success(f'В сообщение "{message.id}" были очищены все реакции — Запросил пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            await self.reactions_helper(ctx)

def setup(bot):
    bot.add_cog(Reactions(bot))