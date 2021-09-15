import json
import traceback
from core.logger import logger


try:
    with open('./data/imgs.json', 'r') as imgs:
        imgs = json.load(imgs)
except FileNotFoundError:
    logger.error(f'Не удалось загрузить imgs.json - Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

