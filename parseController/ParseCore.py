#coding=utf-8
from BeautifulSoup import BeautifulSoup
from dmo.HtmlTag import HtmlTag
from dao.DaoService import DaoService
from common.CommonUtils import CommonUtils
from dmo.TCrawler import TCrawler
from common.DateUtils import DateUtils
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class ParsCore:

    #注意，模版第一个根节点必须有属性，为id,class,或者其他
    def __init__(self, template, target, crawler):
        self.template = template    #需要解析的模板
        self.target = target    #目标a标签名字
        self.tagList = []
        self.crawler = crawler

    #   解析a标签
    def parseA(self):
        soup = BeautifulSoup(self.template)
        targetTag = soup.find(text=self.target)     #找到目标所在的标签
        if targetTag is None:
            print '找不到对应的标题'
            return
        parent = targetTag.parent
        #向上遍历直到根节点
        while None != parent and parent.name != '[document]':
            self.saveTag(parent)
            parent = parent.parent      #向上遍历
        self.save()

    #保存标签到list中去
    def saveTag(self, tag):
        tagOrder = len(self.tagList)
        dmoTag = HtmlTag()
        dmoTag.tagName = tag.name       #保存标签名
        dmoTag.order = tagOrder         #保存标签顺序
        tagAttrs = [attr[0] for attr in tag.attrs]      #获取标签的所有属性
        #保存标签属性
        if 'id' in tagAttrs:
            dmoTag.attr = 'id'
            dmoTag.attrValue = tag['id']
        elif 'name' in tagAttrs :
            dmoTag.attr = 'name'
            dmoTag.attrValue = tag['name']
        elif 'class' in tagAttrs:
            dmoTag.attr = 'class'
            dmoTag.attrValue = tag['class']
        elif 'href' in tagAttrs:
            dmoTag.attr = 'href'
            dmoTag.attrValue = tag['href']
        self.tagList.append(dmoTag)


    #解析文章内容
    def parseContent(self):
        pass

    #保存到数据库
    def save(self):
        dao = DaoService()
        crawler_parm = (self.crawler.name,self.crawler.url,self.crawler.category_id,self.crawler.author,self.crawler.interval,self.crawler.charset)
        id = dao.insert_t_crawler(crawler_parm)
        tag_parms = CommonUtils.htm_tag_to_parms(self.tagList, id)
        dao.insert_html_tags(tag_parms)




html = """

"""



dao = DaoService()
tag_name = ''
tag_attr = ''
tag_attr_value = ''
tag_parm = (tag_name, tag_attr, tag_attr_value, None, None)
blog_tag_id = dao.insert_html_tag(tag_parm)

crawler = TCrawler()
crawler.name = 'tent_licai'
crawler.url = 'http://finance.qq.com/money/'
crawler.category_id = 17
crawler.author = '腾讯网'
crawler.interval = 5
crawler.blog_tag_id = blog_tag_id
p = ParsCore(html, '人民币资产已成“地上悬河”？', crawler)
p.parseA()


