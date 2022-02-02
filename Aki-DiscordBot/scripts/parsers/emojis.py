import json
import traceback
from core.logger import logger


try:
    with open('./data/emojis.json', 'r') as emojis:
        emojis = json.load(emojis)

except FileNotFoundError:
    logger.error(f'Не удалось загрузить emojis.json — Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

