from loguru import logger
from scripts.parsers.settings import settings



if settings is None:
    save_logs = False
else:
    save_logs = settings['save_logs']

if save_logs == 'True':
    logger.add('./logs/logs.log', format = '{time} | {level} | {message}', rotation = '06:00', compression = 'zip')
