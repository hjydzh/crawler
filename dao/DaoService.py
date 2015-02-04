#coding=utf-8
from daoBase.DaoBaseService import DaoBaseService
from common.SqlConstants import SqlConstants
from common.CommonUtils import CommonUtils

class DaoService:
    def insert_html_tags(self, parms):
        dao = DaoBaseService()
        dao.insert(SqlConstants.INSERT_HTML_TAGS, parms)

    def insert_html_tag(self, parm):
        dao = DaoBaseService()
        return dao.insert_id(SqlConstants.INSERT_HTML_TAGS, parm)

    def insert_t_crawler(self, parm):
        dao = DaoBaseService()
        return dao.insert_id(SqlConstants.INSERT_T_CRAWLER, parm)

    #根据模板爬虫id查询爬虫拥有的标签
    def query_tags_by_crawler_id(self, id):
        dao = DaoBaseService()
        obj = dao.query(SqlConstants.QUERY_HTML_TAGS_BY_T_CRAWLER_ID % id)
        return CommonUtils.query_result_to_tags(obj)

    #根据id查询标签
    def query_tag_by_id(self, id):
        dao = DaoBaseService()
        obj = dao.query(SqlConstants.QUERY_HTML_TAG_BY_ID % id)
        return CommonUtils.query_result_to_tag(obj[0])


    def insert_blog(self, blog):
        dao = DaoBaseService()
        parm = (blog._Blog__title, blog._Blog__author,  blog._Blog__content, blog._Blog__weight,  blog._Blog__url, blog._Blog__category_id)
        return dao.insert_id(SqlConstants.INSERT_BLOG, parm)

    #查询文章是否已经存在
    def isBlogExistByTitle(self, title):
        dao = DaoBaseService()
        obj = dao.query(SqlConstants.IS_BLOG_EXIST_BY_TITLE % title)
        num = obj[0][0]
        if num == 0:
            return False
        else:
            return True

    #查询指定目录下一定数量的模板爬虫
    def query_tcrawlers_category(self, id, blog_num):
        dao = DaoBaseService()
        obj = dao.query(SqlConstants.QUERY_TCRAWLERS_CATEGORY % (id, blog_num))
        return CommonUtils.query_result_to_t_crawlers(obj)

    #根据爬虫id查询爬虫
    def query_tcrawler_by_id(self, id):
        dao = DaoBaseService()
        obj = dao.query(SqlConstants.QUERY_TCRAWLER_BY_ID % (id))
        return CommonUtils.query_result_to_t_crawler(obj[0])

    #更新模板爬虫的执行时间
    def update_time_t_crawler(self, crawler_id, next_run_time):
        dao = DaoBaseService()
        dao.update(SqlConstants.UPDATE_TIME_T_CRAWLER % ( next_run_time, crawler_id))

    #更新目录的执行时间
    def update_time_category(self, category_id, next_run_time):
        dao = DaoBaseService()
        dao.update(SqlConstants.UPDATE_TIME_CATEGORY % ( next_run_time, category_id))

    #文章发布到首页推荐区
    def update_portal_show(self, blog_id):
        dao = DaoBaseService()
        dao.update(SqlConstants.UPDATE_PORTAL_SHOW % blog_id)

    #删除文章
    def delete_blog(self, blog_id):
        dao = DaoBaseService()
        dao.delete(SqlConstants.DELETE_BLOG % blog_id)

    #查询所有二级目录
    def query_categories(self):
        dao = DaoBaseService()
        obj = dao.query(SqlConstants.QUERY_CATEGORIES_BY_ID % 2)
        return CommonUtils.query_result_to_categories(obj)
