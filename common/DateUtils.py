#coding=utf-8
import datetime
import time
class DateUtils:

    STYLE1 = "%Y%m%d%H%M%S"

    STYLE_MYSQL = "%Y-%m-%d %H:%M:%S"

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
    def date_of_str_format(date, style):
        return date.strftime(style)

    #增加指定天数
    @staticmethod
    def add_day(date, day):
        return  date + datetime.timedelta(days=day)
if __name__ == '__main__':
    now =  DateUtils.now()
    now = DateUtils.add_day(now, 2)
    print DateUtils.date_of_str_format(now, DateUtils.STYLE_MYSQL)
