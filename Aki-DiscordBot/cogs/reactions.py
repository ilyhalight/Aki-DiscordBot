import discord

from discord.ext import commands

from core.bot import avatar
from core.logger import logger
from data.colors import colors
from scripts.parsers.settings import settings

emoji_add = ["добавить"]
emoji_del = ["удалить", "стереть", "очистить"]
emoji_clear = ["удалить_всё", "стереть_всё", "очистить_всё", "удалить_все", "стереть_все", "очистить_все"]

class Reactions(commands.Cog):
    """Взаимодействие с эмоджи"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [
                                'emoji', 'reaction', 'react',
                                'эмодзи', 'эмоджи', 'реакция', 'реакт'
                                ])
    @commands.has_permissions(administrator = True)
    async def reactions_command(self, ctx, act: str = None, id: int = None, reaction: str = None):
        if act != None and id != None:
            await ctx.message.delete()
            message = await ctx.message.channel.fetch_message(id)
            if act.lower() in emoji_add and reaction != None:
                await message.add_reaction(reaction)
                logger.success(f'К сообщению "{message.id}" была добавлена реакция "{reaction}" - Пользователь: {ctx.author} ({ctx.author.id}).')
            if act.lower() in emoji_del and reaction != None:
                await message.clear_reaction(reaction)
                logger.success(f'В сообщение  "{message.id}" были очищены реакции "{reaction}" - Пользователь: {ctx.author} ({ctx.author.id}).')
            if act.lower() in emoji_clear:
                await message.clear_reactions()
                logger.success(f'В сообщение "{message.id}" были очищены все реакции - Пользователь: {ctx.author} ({ctx.author.id}).')
        else:
            emb = discord.Embed(title = 'Помощник - Реакции', color = colors['help'])
            emb.add_field(name = 'Использование', value = f'`{settings["prefix"]}реакция <действие> <id сообщения> <реакция>`\n┗ Произведёт действие с реакциями в сообщение с заданным айди.', inline = False)
            emb.add_field(name = 'Пример 1', value = f'`{settings["prefix"]}реакция добавить 824428281104564264 :thumbsup:`\n┗ Добавит к сообщению с заданным айди реакцию :thumbsup:.', inline = False)
            emb.add_field(name = 'Пример 2', value = f'`{settings["prefix"]}реакция очистить 824428281104564264 :thumbsup:`\n┗ Очистит в сообщение с заданным айди определнные реакции :thumbsup:.', inline = False)
            emb.add_field(name = 'Пример 3', value = f'`{settings["prefix"]}реакция очистить_все 824428281104564264`\n┗ Очистит в сообщение с заданным айди абсолютно все реакции.', inline = False)
            emb.set_footer(text = 'Aki © 2021 Все права защищены', icon_url = avatar(self.bot.user))
            emb.set_thumbnail(url = avatar(self.bot.user))
            await ctx.send(embed = emb)
            logger.info(f'Информация о "реакция" - Пользователь: {ctx.author} ({ctx.author.id}).')

def setup(bot):
    bot.add_cog(Reactions(bot))