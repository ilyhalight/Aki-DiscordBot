import json

from core.logger import logger



try:
    with open('./data/imgs.json', 'r') as imgs:
        imgs = json.load(imgs)
except:
    imgs = {
            "backup":   "",
            "no_permissions":   "",
            "success": "",
            "error": "",
            "help": "",
            "tinyurl" :   ""
    }
    logger.error(f'Не удалось загрузить imgs.json - Пользователь: SYSTEM.')