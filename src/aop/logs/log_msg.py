import logging
import logging.handlers as handlers


class LogMsgs:
    def __init__(self):
        self.logger = logging.getLogger('data_automation')
        self.logger.setLevel(logging.INFO)
        self.logHandler = handlers.RotatingFileHandler('app_debug.log', maxBytes=500)

        self.formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:(%(lineno)d):%(message)s')
        self.logHandler.setLevel(logging.INFO)

        # Here we set our logHandler's formatter
        self.logHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.logHandler)

    def logs_msg(self, msg=None):
        logging.info(msg)
        self.logger.info(msg)
