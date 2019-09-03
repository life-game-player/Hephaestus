import logging
import logging.handlers


# 配置logger
logging_handler = logging.handlers.RotatingFileHandler(
    'logs/volcano.log',
    'a',
    1024 * 1024,
    10,
    'utf-8'
)
logging_format = logging.Formatter(
    '%(asctime)s [%(name)s - %(levelname)s] %(message)s'
)
logging_handler.setFormatter(logging_format)
logger = logging.getLogger()
logger.addHandler(logging_handler)
logger.setLevel(logging.DEBUG)
