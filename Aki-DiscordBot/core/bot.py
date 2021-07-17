from discord.ext import commands

from scripts.parsers.settings import settings
from scripts.parsers.owner import owner



bot = commands.Bot(command_prefix = settings['prefix'], case_insensitive = True)
bot.remove_command('help') # Удаляем встроенную команду хелп

def is_owner(id):
    if id == owner['id']:
        return True
    else:
        return False