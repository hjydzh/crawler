#coding=utf-8
import logging
import logging.config
class Log:

    @staticmethod
    def log():
        logging.config.fileConfig("logger.conf")
        a = logging.getLogger("root")
        return a

