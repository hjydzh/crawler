#encoding=utf-8
import jieba
import copy
from WordInfo import WordInfo
from SearchCore import SearchCore
from dao.DaoService import DaoService
from requestController.RequestCore import RequestCore
import traceback
from log.Log import Log
import logging
class HotSearchCore:

    def __init__(self):
        self.word_list = {}
        self.search_core = SearchCore()
        self.crawlers = {}

    def hot_search(self, ids):
        Log.init_log()
        for id in ids:
            crawlers = self.get_crawler_category(id)
            for crawler in crawlers:
                logging.debug('name:%s, url:%s' % (crawler.author, crawler.url))
                if None is crawler.url or '' == crawler.url:
                    #如果爬虫没有url，则不执行
                    continue
                if crawler.charset != 'utf-8':
                    #只处理utf-8爬虫
                    continue
                try:

                    self.parse(crawler)
                except Exception as err:
                    logging.debug(traceback.format_exc())
                self.crawlers[crawler.id] = crawler
        self.sort_word_list()
        url = self.find_hot_url()
        logging.debug('最热文章url为:')
        logging.debug(url)
        crawler_id = self.get_crawler_id(url)
        real_url = self.get_real_url(url)
        crawler = self.crawlers[int(crawler_id)]
        self.search_core.crawler = crawler
        blog = self.get_blog(self.get_title(url), real_url)
        self.save(blog)
        logging.debug('最热文章更新成功')


    def save(self, blog):
        if None is blog:
            return
        dao = DaoService()

        self.search_core.save_blog(blog)

    #查询某个目录下的所有爬虫
    def get_crawler_category(self, id):
        dao = DaoService()
        return dao.query_all_tcrawlers_category(id)

    #给url加上所属爬虫id极其标题
    def get_id_url(self, crawler, url, title):
        return str(url) + '|' + str(crawler.id) + '|' + title.encode('utf-8')

    #从url中解析出爬虫id
    def get_crawler_id(self, url):
        return  url.split('|')[1]

    #从url中解析出实际url
    def get_real_url(self, url):
         return  url.split('|')[0]

    #从url中解析出标题
    def get_title(self, url):
        return  url.split('|')[2].decode('utf-8')

    #根据url获取blog
    def get_blog(self, title, url):
        self.search_core.get_tag_list()
        return self.search_core.fetchBlog(title, url)

    #解析某个网站的文章，词添加到全局词典中
    def parse(self, crawler):
        self.search_core.crawler = crawler
        search_core = self.search_core
        search_core.get_tag_list()
        search_core.get_html()
        templates = search_core.search_templates()
        for template in templates[:10]:
            tag = search_core.get_tag(template)
            if tag != None:
                words = self.title_parse(tag.text)  #得到词列表
                href = RequestCore.getRealUrl(tag['href'], crawler.url)
                url = self.get_id_url(crawler,href,tag.text)
                self.word_add(words, url, crawler)   #词更新到词典


    #解析文章标题
    def title_parse(self, title):
        return jieba.cut(title)

    #新增词组
    def word_add(self, words, url, crawler):
        for word in words:
            if(len(word) <=1):
                #如果单词只有一个汉字，则不加入到词典中去
                continue
            if(word == 'O2O'):
                #由于亿欧网存在大量o2o关键词，故过滤o2o
                continue
            word_info = self.find_word(word, url)
            self.word_list[word] = word_info


    #查找词，如果存在，则在其信息中计数加1.不存在则返回生成的词信息
    def find_word(self, word, url):
        word_info = self.word_list.get(word)
        if None is not word_info:
            word_info.num = word_info.num + 1
            word_info.url_list.add(url)
        else:
            word_info =  WordInfo(word, url)
        return word_info

    #根据单词出现的次数从大到小排序
    def sort_word_list(self):
        self.word_list = sorted(self.word_list.iteritems(), key=lambda item : item[1].num, reverse=True)

    #寻找拥有2个最热词的文章地址,即一个文章拥有第一和第二热词
    def find_hot_url(self):
        word_info = self.word_list[0][1]
        first_url_list = word_info.url_list
        if len(first_url_list) == 1:
            return first_url_list[0]
        word_info = self.word_list[1][1]
        sec_hot_url_list = word_info.url_list
        for url in first_url_list:
            #如果在第二热词中的url存在一致的url，则返回此 url
            if url in sec_hot_url_list:
                return url
        return first_url_list.pop()


if __name__ == '__main__':
    s = HotSearchCore()
    ids = [6, 7]
    s.hot_search(ids)