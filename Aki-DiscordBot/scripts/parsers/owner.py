import json
import traceback
from core.logger import logger


try:
    with open('./data/owner.json', 'r') as owner:
        owner = json.load(owner)
except FileNotFoundError:
    logger.error(f'Не удалось загрузить owner.json - Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

