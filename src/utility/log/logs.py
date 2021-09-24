import logging
import logging.handlers as handlers

logger = logging.getLogger('data_automation')
logger.setLevel(logging.INFO)
logHandler = handlers.RotatingFileHandler('app_debug.log', maxBytes=500)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:(%(lineno)d):%(message)s')
logHandler.setLevel(logging.INFO)

# Here we set our logHandler's formatter
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


def logs_msg(msg=None):
    logging.info(msg)
    logger.info(msg)


def logs_warning(warning=None):
    logging.warning(warning)
    logger.warning(warning)


def logs_error(error=None):
    logging.error(error)
    logger.error(error)
