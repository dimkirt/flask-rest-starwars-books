import sys
import logging


def create_logger(module_name):
    # Initialize logger
    logger = logging.getLogger('root.{}'.format(module_name))
    logger.setLevel(level=logging.INFO)
    console_handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger
