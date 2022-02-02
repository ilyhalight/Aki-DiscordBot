import json
import traceback
from core.logger import logger


try:
    with open('./data/status.json', 'r') as status_json:
        status = json.load(status_json)
except FileNotFoundError:
    logger.error(f'Не удалось загрузить status.json — Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')


def update_status(data):
    with open('./data/status.json', 'w') as status_json:
        status_json.write(json.dumps(data, indent=4))

