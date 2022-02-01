import os
import sys
from loguru import logger
from scripts.parsers.settings import settings


if settings is None:
    save_logs = False
    debug = False
else:
    save_logs = settings['save_logs']
    debug = settings['debug']

if not debug:
    logger.remove(0)
    logger.add(sys.stderr, level="INFO")

if save_logs:
    if not os.path.isdir('./logs'):
        os.mkdir('./logs')
    logger.add('./logs/logs.log', format = '{time} | {level} | {message}', rotation = '06:00', compression = 'zip')

