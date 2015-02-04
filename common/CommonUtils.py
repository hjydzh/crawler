from dmo.HtmlTag import HtmlTag
from dmo.TCrawler import TCrawler
from dmo.Category import Category
class CommonUtils:

    @staticmethod
    def htm_tag_to_parms(html_tags,crawler_id):
        parms = []
        for tag in html_tags:
            parm = (tag.tagName, tag.attr, tag.attrValue, tag.order, crawler_id)
            parms.append(parm)
        return parms

    @staticmethod
    def query_result_to_tags(results):
        tags = []
        for result in results:
            tag = CommonUtils.query_result_to_tag(result)
            tags.append(tag)
        return tags

    @staticmethod
    def query_result_to_tag(result):
        tag = HtmlTag()
        tag.tagName = result[0]
        tag.attr = result[1]
        tag.attrValue = result[2]
        tag.order = result[3]
        return tag


    @staticmethod
    def query_result_to_t_crawlers(results):
        crawlers = []
        if None is results:
            return crawlers
        for result in results:
            crawler = CommonUtils.query_result_to_t_crawler(result)
            crawlers.append(crawler)
        return crawlers


    @staticmethod
    def query_result_to_t_crawler(result):
        if None is result:
            return None
        crawler = TCrawler()
        crawler.id =  result[0]
        crawler.name =  result[1]
        crawler.url =  result[2]
        crawler.category_id =  result[3]
        crawler.author =  result[4]
        crawler.next_run_time =  result[5]
        crawler.interval =  result[6]
        crawler.charset =  result[7]
        crawler.filter_words =  result[8]
        crawler.blog_tag_id = result[9]
        return crawler

    @staticmethod
    def query_result_to_categories(results):
        categories = []
        for result in results:
            category = Category()
            category.category_id =  result[0]
            category.category_name =  result[1]
            category.next_run_time =  result[2]
            category.interval =  result[3]
            category.update_blog_num =  result[4]
            categories.append(category)
        return categories

