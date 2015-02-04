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

<div class="entry" style="position: absolute; left: 180px; top: 0px;">
							<div class="entry-img">
								<a href="http://www.vcbeat.net/9905.html" target="_blank">
									<img class="" width="230" height="150" src="http://www.vcbeat.net/wp-content/uploads/2015/02/hipaa.png" alt="全面解读HIPAA三大目的">
								</a>
								<div id="bdshare" class="bdshare_t bds_tools get-codes-bdshare" data="{'text':'全面解读HIPAA三大目的',
										'pic':'http://www.vcbeat.net/wp-content/uploads/2015/02/hipaa-209x150.png'}">
								    <span class="bds_more glyphicon glyphicon-share"></span>
								</div>
							</div>

							<div class="entry-detail">
								<div class="entry-meta-mobile">
									<a href="http://www.vcbeat.net/category/%e5%8a%a8%e8%84%89%e5%a4%b4%e6%9d%a1">动脉头条</a> /
									1天前								</div>

								<h3 class="entry-title">
									<a href="http://www.vcbeat.net/9905.html" target="_blank">全面解读HIPAA三大目的</a>
								</h3>

								<a class="entry-excerpt" href="http://www.vcbeat.net/9905.html" target="_blank">
									<p>HIPAA 全称是Health Insurance Portability and Accountability Act/1996，中文翻译应该是健康保险连续和责任法案，1996年由美国国会通过，比尔克林顿总统签署生效。</p>
								</a>

								<div class="entry-meta-pc">
									1天前									<a href="http://www.vcbeat.net/9905.html#respond" class="entry-comment" target="_blank">
										<span class="glyphicon glyphicon-comment"></span>
									</a>
								</div>
							</div>
						</div>



"""



dao = DaoService()
tag_name = 'div'
tag_attr = 'id'
tag_attr_value = 'post-content'
tag_parm = (tag_name, tag_attr, tag_attr_value, None, None)
blog_tag_id = dao.insert_html_tag(tag_parm)
print blog_tag_id

crawler = TCrawler()
crawler.name = 'dongmai_common'
crawler.url = 'http://www.vcbeat.net/'
crawler.category_id = 9
crawler.author = '动脉网'
crawler.interval = 2
crawler.blog_tag_id = blog_tag_id
p = ParsCore(html, '全面解读HIPAA三大目的', crawler)
p.parseA()


