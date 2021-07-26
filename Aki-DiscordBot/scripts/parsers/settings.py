import json
from loguru import logger



try:
    with open('./data/settings.json', 'r') as settings:
        settings = json.load(settings)
except:
    settings = {
            "backup": False,
            "debug": False,
            "save_logs": False,
            "full_logs": False,
            "prefix": "$"
            }
    logger.error(f'Не удалось загрузить settings.json - Пользователь: SYSTEM.')