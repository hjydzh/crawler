#coding=utf-8
import datetime
import time
class DateUtils:
    @staticmethod
    def now():
        return datetime.datetime.now()

    @staticmethod
    def date_of_str():
        return DateUtils.now().strftime("%Y%m%d%H%M%S")

    #增加指定天数
    @staticmethod
    def add_day(date, day):
        return  date + datetime.timedelta(days=day)
if __name__ == '__main__':
    print DateUtils.date_of_str()
