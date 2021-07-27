import os
from zipfile import ZipFile

from core.logger import logger



def create_archive(folder):
    try:
        zip = ZipFile(f'{folder}.zip', 'w')
        for root, dirs, files in os.walk(folder):
            for file in files:
                zip.write(os.path.join(root,file))
                zip.close
        logger.success('ZIP-архив создан - Пользователь: SYSTEM')
    except:
        logger.error('Не удалось создать ZIP-архив - Пользователь: SYSTEM')