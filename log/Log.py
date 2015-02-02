#coding=utf-8
import logging
import logging.config
import os
class Log:

    @staticmethod
    def init_log():
        logging.config.fileConfig("logger.conf")
        logging.getLogger("root")
