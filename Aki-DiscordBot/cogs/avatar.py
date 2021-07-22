import discord

from discord.ext import commands

from core.bot import avatar
from core.logger import logger
from scripts.parsers.settings import settings
from data.colors import colors

class Avatar(commands.Cog):
    """Show user avatar"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = [
                                'avatarka', 'ava', 'avatar',
                                'аватарка', 'ава', 'аватар'
                                ])
    async def avatar_command(self, ctx, member: discord.Member = None):
        if member == None:
            user = ctx.message.author
        else:
            user = member
        emb = discord.Embed(title = f'Аватар пользователя {user}', colour = colors['black'])
        emb.set_image(url = avatar(user))
        await ctx.send(embed = emb)
        logger.info(f'Выведен аватар пользователя {user} - Пользователь {ctx.author} запросил аватар.')

def setup(bot):
    bot.add_cog(Avatar(bot))