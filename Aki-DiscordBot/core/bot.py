from discord.ext import commands

from scripts.parsers.settings import settings
bot = commands.Bot(command_prefix = prefix, case_insensitive = True)
bot.remove_command('help') # Удаляем встроенную команду хелп