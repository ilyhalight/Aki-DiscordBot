from discord.ext import commands

bot = commands.Bot(command_prefix = prefix, case_insensitive = True)
bot.remove_command('help') # Удаляем встроенную команду хелп