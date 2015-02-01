from dmo.HtmlTag import HtmlTag
from dmo.TCrawler import TCrawler
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
    def query_result_to_t_crawler(results):
        crawlers = []
        for result in results:
            crawler = TCrawler()
            crawler.id =  result[0]
            crawler.name =  result[1]
            crawler.url =  result[2]
            crawler.category_id =  result[3]
            crawler.author =  result[4]
            crawler.run_time =  result[5]
            crawler.interval =  result[6]
            crawler.charset =  result[7]
            crawler.filter_words =  result[8]
            crawler.blog_tag_id = result[9]
            crawlers.append(crawler)
        return crawlers