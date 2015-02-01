#coding=utf-8
from searchController.SearchCore import SearchCore
from common.DateUtils import DateUtils
from dao.DaoService import DaoService
from searchController.SearchCore import SearchCore
import traceback
import logging
import logging.config
from log.Log import Log
#检查爬虫是否允许执行
def check_run_status(crawler):
    run_time = crawler.run_time
    interval = crawler.interval
    nex_run_time = DateUtils.add_day(run_time, interval)
    if nex_run_time > DateUtils.now():
        return False
    return True

def crawler_run(crawler):
    search = SearchCore(crawler)
    search.search()


logging.config.fileConfig("logger.conf")
logging.getLogger("root")
dao = DaoService()
crawlers = dao.queryTCrawlers()
for crawler in crawlers:
    if check_run_status(crawler):
        try:
            logging.debug('执行')
            logging.info(crawler.name)
            crawler_run(crawler)
            #更新爬虫执行时间
            dao.update_time_t_crawler(crawler.id)
        except Exception as err:
            logging.error('执行出错')
            logging.error(traceback.format_exc())
            logging.error( err)

