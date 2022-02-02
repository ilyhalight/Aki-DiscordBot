import json
import traceback
from core.logger import logger


try:
    with open('./data/guild/verification_level.json', 'r') as verification_level:
        verification_level = json.load(verification_level)

except FileNotFoundError:
    logger.error(f'Не удалось загрузить verification_level.json — Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

