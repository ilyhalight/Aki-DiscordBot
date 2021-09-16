import os
import traceback
from zipfile import ZipFile

from core.logger import logger


def create_archive(folder):
    try:
        zip = ZipFile(f'{folder}.zip', 'w')
        for root, dirs, files in os.walk(folder): # Не убирайте dirs, иначе будет вылетать ошибка
            for file in files:
                zip.write(os.path.join(root, file))
                zip.close
        logger.success('ZIP-архив создан - Пользователь: SYSTEM')
    except ValueError:
        logger.error('Не удалось создать ZIP-архив - Пользователь: SYSTEM')
        logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

