import logging

from logging.handlers import RotatingFileHandler

# Создание и настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание обработчика для вывода логов на консоль

file_handler = RotatingFileHandler('logfile.txt', encoding='utf-8',
                                   maxBytes=1024 * 1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)

# Создание форматирования для сообщений в логе
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(file_handler)
