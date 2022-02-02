import json
import traceback
from core.logger import logger


try:
    with open('./data/backups.json', 'r') as backups:
        backups = json.load(backups)
except FileNotFoundError:
    logger.error(f'Не удалось загрузить backups.json — Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

