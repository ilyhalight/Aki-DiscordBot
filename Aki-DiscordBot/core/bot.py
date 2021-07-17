from discord.ext import commands

from scripts.parsers.settings import settings



bot = commands.Bot(command_prefix = settings['prefix'], case_insensitive = True)
bot.remove_command('help') # Удаляем встроенную команду хелп

def is_owner(id):
    if id == INFO['owner_id']:
        return True
    else:
        return False