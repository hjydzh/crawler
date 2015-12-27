#coding=utf-8
import datetime
import time
class DateUtils:

    STYLE1 = "%Y%m%d%H%M%S"

    STYLE_MYSQL = "%Y-%m-%d %H:%M:%S"

    STYLE_YM = "%Y%m"

    STYLE_YMD = '%Y-%m-%d'

    @staticmethod
    def now():
        return datetime.datetime.now()

    @staticmethod
    def now_format(style):
        return DateUtils.now().strftime(style)

    @staticmethod
    def date_of_str():
        return DateUtils.now().strftime("%Y%m%d%H%M%S")

    @staticmethod
    def day_now_str(style):
        return DateUtils.now().strftime(style)

    @staticmethod
    def date_of_str_format(date, style):
        return date.strftime(style)

    #增加指定天数
    @staticmethod
    def add_day(date, day):
        return  date + datetime.timedelta(days=day)

    @staticmethod
    def get_month():
        return DateUtils.now().strftime(DateUtils.STYLE_YM)
if __name__ == '__main__':
    print DateUtils.now_format("%H:%M:%S")
