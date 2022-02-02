from discord.ext import commands

from scripts.parsers.settings import settings
from scripts.parsers.owner import owner


bot = commands.Bot(command_prefix = settings['prefix'], case_insensitive = True)
bot.remove_command('help') # Удаляем встроенную команду хелп

def cog_values():
    """Показываем кол-во когов"""

    cog_values = len(bot.cogs)
    return cog_values

def commands_values():
    """Показываем кол-во команд доступных в боте"""

    commands_values = len(bot.commands)
    return commands_values

def server_number():
    """Показываем кол-во серверов на которых находится бот"""

    server_number = len(bot.guilds)
    return server_number

def server_members(guild_id: int = None):
    """
    Показываем кол-во участников на сервере

    Args:
        guild_id (int): id гильдии
    """

    server_members = len(guild_id.members)
    server_members = server_members + 1
    return server_members

def avatar(id: int):
    """
    Показываем аватарку участника или сервера

    Args:
        id (int): id участника или гильдии
    """
    avatar = id.avatar_url
    return avatar

def is_owner(user_id: int):
    """
    Проверка, является ли участник создателем

    Args:
        user_id (int): id участника

    Examples:
        is_owner(ctx.author.id)

    Returns:
        boolean:
            True: id участника совпал с id создателя;
            False: id участника не совпал с id создателя;
    """

    if user_id == owner['id']:
        return True
    else:
        return False