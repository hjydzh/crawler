__author__ = 'junyu'
import os
import logging
import logging.config
class Log:
    @staticmethod
    def init_log():
        file_path = os.path.abspath(os.path.dirname(__file__))
        logging.config.fileConfig(file_path + '\logger.conf')
        logging.getLogger("root")

