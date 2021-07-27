import json
from loguru import logger



try:
    with open('./data/backups.json', 'r') as backups:
        backups = json.load(backups)
except:
    backups = [
            "data",
            "cogs",
            "core",
            "scripts"
            ]
    logger.error(f'Не удалось загрузить backups.json - Пользователь: SYSTEM.')