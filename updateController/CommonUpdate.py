#coding=utf-8
from searchController.SearchCore import SearchCore
from common.DateUtils import DateUtils
from dao.DaoService import DaoService
from searchController.SearchCore import SearchCore
from log.Log import Log
import traceback
import logging

class CommonUpdate:
    def __init__(self):
        self.dao = DaoService()

    def update_website(self):
        Log.init_log()
        logging.debug("网站内容更新开始")
        categories = self.get_categories()
        for category in categories:
            self.update_category(category)
        logging.debug("网站内容更新完成")


    #查询所有二级目录
    def get_categories(self):
        return self.dao.query_categories()

    #更新一个目录
    def update_category(self, category):
        category_id = category.category_id
        blog_num = category.update_blog_num
        crawlers = self.dao.query_tcrawlers_category(category_id, blog_num)
        if not crawlers:
            return
        for crawler in crawlers:
            try:
                logging.debug('执行')
                logging.info(crawler.name)
                self.crawler_run(crawler)
                next_run_time = self.get_next_run_time(crawler.interval)
                self.dao.update_time_t_crawler(crawler.id, next_run_time)
            except Exception as err:
                logging.error('执行出错')
                logging.error(traceback.format_exc())
                logging.error( err)
        next_run_time = self.get_next_run_time(category.interval)
        self.dao.update_time_category(category_id, next_run_time)



    #执行爬虫
    def crawler_run(self, crawler):
        search = SearchCore(crawler)
        search.search()

    #获得下次执行时间
    def get_next_run_time(self, interval):
        now = DateUtils.now()
        next_run_time = DateUtils.add_day(now, interval)
        return DateUtils.date_of_str_format(next_run_time, DateUtils.STYLE_MYSQL)


