import os
import shutil
from datetime import datetime
import traceback

from core.logger import logger
from scripts.parsers.info import info
from scripts.parsers.settings import settings
from scripts.parsers.backups import backups
from scripts.checks import is_python_file, is_json_file
from scripts.archive import create_archive


def create_backup():
    '''Создаёт бэкап заданных папок'''

    time = datetime.now().strftime(settings['time_format'])
    backup_dir = f'./backups/Aki {info["status"]} {info["version"]} {time}'

    if os.path.isdir('./backups'):
        pass
    else:
        try:
            os.mkdir('./backups')
            logger.info('Папка для бэкапов создана - Пользователь: SYSTEM')
        except:
            logger.error('Не удалось создать папку для бэкапов - Пользователь: SYSTEM')
            logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
    try:
        os.makedirs(backup_dir)
        logger.info(f'Папка {backup_dir} создана - Пользователь: SYSTEM')
        try:
            for dir in backups:
                os.makedirs(f'{backup_dir}\\{dir}')
                logger.info(f'Папка {backup_dir}\\{dir} создана - Пользователь: SYSTEM')
            logger.success('Все папки для бэкапа созданы - Пользователь: SYSTEM')
            try:
                shutil.copy2('main.py', backup_dir)
                for dir in backups:
                    for file in os.listdir(f'.\\{dir}'):
                        if is_python_file(file) or is_json_file(file):
                            shutil.copy2(f'.\\{dir}\{file}', f'.\\{backup_dir}\{dir}')
                logger.success('Все файлы для бэкапа скопированы - Пользователь: SYSTEM')
                create_archive(backup_dir)
                logger.success(f'Архив {backup_dir} создан - Пользователь: SYSTEM')
                try:
                    shutil.rmtree(backup_dir)
                    logger.success('Остатки от бэкапа удалены - Пользователь: SYSTEM')
                except:
                    logger.error(f'Не удалось удалить остатки от бэкапа удалены ({backup_dir}) - Пользователь: SYSTEM.')
                    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
            except FileNotFoundError:
                logger.error('Не удалось скопировать все файлы для бэкапа - Пользователь: SYSTEM.')
                logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
        except:
            logger.error(f'Не удалось создать папку {dir} в {backup_dir} - Пользователь: SYSTEM.')
            logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
    except:
        logger.error(f'Не удалось создать папку {backup_dir} - Пользователь: SYSTEM.')
        logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

    logger.success('Бэкап успешно создан - Пользователь: SYSTEM.')

