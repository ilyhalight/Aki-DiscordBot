import json

from core.logger import logger



try:
    with open('./data/owner.json', 'r') as owner:
        owner = json.load(owner)
except:
    status = {
            "id": 551653500216672256,
            "name": "Toil",
            "tag": 8997
            }
    logger.error(f'Не удалось загрузить owner.json - Пользователь: SYSTEM.')