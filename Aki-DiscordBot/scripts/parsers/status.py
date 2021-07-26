import json

from core.logger import logger



try:
    with open('./data/status.json', 'r') as status_json:
        status = json.load(status_json)
except:
    status = {
            "status": " ",
            "active": 1,
            "link": None,
            "text": None
            }
    logger.error(f'Не удалось загрузить status.json - Пользователь: SYSTEM.')

def update_status(data):
    with open('./data/status.json', 'w') as status_json:
        status_json.write(json.dumps(data, indent=4))