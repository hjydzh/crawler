#coding=utf-8
__author__ = 'junyu'
from dmo.HtmlTag import HtmlTag
from dao.DaoService import DaoService
from dmo.Blog import Blog
from requestController.RequestCore import RequestCore
import re
import time
from common.DateUtils import DateUtils
from oss.oss_api import *
import logging
from log.Log import Log
import traceback
class SearchCore:


    def __init__(self, crawler):
        self.tagList = []
        self.crawler = crawler
        self.img_list = []
        self.img_time = None
        self.blog_content_tag = None

    #查询tag列表
    def get_tag_list(self):
        dao = DaoService()
        self.tagList = dao.query_tags_by_crawler_id(self.crawler.id)
        self.blog_content_tag = dao.query_tag_by_id(self.crawler.blog_tag_id)

    #获得目标url的html
    def get_html(self):
        url = self.crawler.url
        logging.debug("请求url:")
        logging.debug(url)
        self.html = RequestCore.request(url, self.crawler.charset)

    def search(self):
        Log.init_log()
        logging.debug('开始抓取')
        self.get_tag_list()
        self.get_html()
        #self.tagList = self.tagList[::-1]
        templates = self.search_templates()
      #  self.tagList = self.tagList[1:]
        tag = None
        for template in templates[1:]:
            tag = self.get_tag(template)
            if tag != None:
                blog = self.fetchBlog(tag)
                self.save_blog(blog)
                break


    # 保存文章
    def save_blog(self, blog):
        dao = DaoService()
        if not dao.isBlogExistByTitle( blog._Blog__title):
            logging.debug("博客不存在数据库，开始更新，更新博客题目为:" + blog._Blog__title)
            blog_id = dao.insert_blog(blog)
            #上传图片
            try:
                self.upload_pic()
            except Exception :
                logging.error('上传图片出错')
                logging.error(traceback.format_exc())
                #删除已经插入的文章
                dao.delete_blog(blog_id)
                return

            #文章发布到首页
            dao.update_portal_show(blog_id)


    #访问a标签，并获取网页正文
    def fetchBlog(self, aTag):
        blog = Blog()
        blog._Blog__url = RequestCore.getRealUrl(aTag['href'], self.crawler.url)
        blog._Blog__title = aTag.text
        blog._Blog__weight = 0
        blog._Blog__category_id = self.crawler.category_id
        blog._Blog__author = self.crawler.author
        logging.debug("访问文章所在网站，地址为:" +  blog._Blog__url)
        html = RequestCore.request(blog._Blog__url, self.crawler.charset)
        blog._Blog__content = self.searchContent(html)
        return blog

    #
    def searchContent(self, html):
        soup = ''
        content_soup = self.get_content_soup(soup)
        self.filter_script(content_soup)
        self.filter_words(content_soup)
        self.get_img_url(content_soup)
        return content_soup

    #过滤script标签
    def filter_script(self, soup):
        script_tags = soup.findAll("script")
        if script_tags != None:
            for script in script_tags:
                if script != None:
                    script.extract()

    #过滤a标签
    def filter_a(self, soup):
        script_tags = soup.findAll("a")
        if script_tags != None:
            for script in script_tags:
                if script != None:
                    logging.debug("替换a标签为文本:" + script.text)
                    script.replaceWith(script.text)

    #过滤含有关键词的标签
    def filter_words(self, soup):
        words = self.crawler.filter_words
        if None == words:
            return
        words = words.split()
        for word in words:
            self.remove_word_tag(soup, word)

    #保存
    def get_img_url(self, soup):
        img_tags = soup.findAll("img")
        self.img_time = DateUtils.date_of_str()
        i = 0
        if None != img_tags:
            for img in img_tags:
                self.img_list.append(img['src'])
                img['src'] = 'http://weis-pic.oss-cn-qingdao.aliyuncs.com/'+ self.img_time + str(i) + '.jpeg'
                i = i + 1

    #删除含有关键字的标签
    def remove_word_tag(self, soup, word):
        txt = u"""[\s\S]*%s[\s\S]*""" % word
        tag = soup.find(text=re.compile(txt))
        if tag is not None:
            tag.parent.extract()

    #根据tag获取文章内容soup对象
    def get_content_soup(self, soup):
        tagName = self.blog_content_tag.tagName
        attr = self.blog_content_tag.attr
        attrValue = self.blog_content_tag.attrValue
        content_soup = soup.find(tagName, {attr : attrValue})
        return content_soup


    def simplyStrategy(self, soup):
        pList = soup.findAll('p')
        if len(pList) < 15:
            return None
        p = pList[len(pList) / 2]
        parent = p.parent
        parent_a_list = parent.findAll('p')
        if len(parent_a_list) < 15:
            return None
        return parent

    #搜索目标节点
    def get_tag(self, template):
        target_tag = self.findTarget(template)
        return target_tag

    #寻找匹配的a标签
    def findTarget(self, soup):
        a_list = soup.findAll('a')
        for a in a_list:
            target = self.loopFind(a)
            if None != target:
                return target
        pass

    #遍历树
    def loopFind(self, child):
        parent = child.parent
        list_tag_index = 1  #数据库中的tag索引
        while None != parent and parent.name != '[document]' and list_tag_index < len(self.tagList):
            if not self.is_match(parent, self.tagList[list_tag_index]):
                return None
            list_tag_index = list_tag_index + 1
            parent = parent.parent
        return child


    #判断节点是否相同
    def is_match(self, beau_tag, list_tag):
        beau_tag_name = beau_tag.name
        list_tag_name = list_tag.tagName
        if beau_tag_name != list_tag_name:
            return False
        if list_tag.attr != '':
            list_tag_attr = list_tag.attr
            list_tag_value = list_tag.attrValue
            beau_tag_value = beau_tag[list_tag_attr]
            if beau_tag_value != list_tag_value:
                return False
        return True

    #搜索符合模版的所有节点
    def search_templates(self):
         soup = ''
         root_tag = self.tagList[-1]
         target_templates =  soup.findAll(root_tag.tagName, attrs={root_tag.attr: root_tag.attrValue})    #找到html中所有匹配的dom树
         return target_templates

    #上传图片
    def upload_pic(self):
        oss = OssAPI("oss-cn-qingdao.aliyuncs.com", "rtquzVvMIXn2a7mB", "DtXVOoWVoBPisuIAyhdjoFlxbv4AnS")
        i = 0
        if self.img_list is None:
            return
        for img_url in self.img_list:
            img= RequestCore.img_request(img_url)
            name = self.img_time + str(i) + '.jpeg'
            logging.debug('开始保存图片，地址为:' + name)
            res = oss.put_object_with_data("weis-pic",  name, img)
            i = i + 1

