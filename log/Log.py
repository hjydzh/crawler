#coding=utf-8
import logging
import logging.config
import os
class Log:

    @staticmethod
    def init_log():
        file_path = os.path.abspath(os.path.dirname(__file__))
        logging.config.fileConfig(file_path + '\logger.conf')
        logging.getLogger("root")
