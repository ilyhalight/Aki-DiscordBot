import json
import traceback
from core.logger import logger


try:
    with open('./data/info.json', 'r') as info:
        info = json.load(info)
except FileNotFoundError:
    logger.error(f'Не удалось загрузить info.json — Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

