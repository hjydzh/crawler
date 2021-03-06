#coding:utf-8
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
class WeiBoCrawler:

    #代理地址
    PROXY_HOST = ''

    #代理端口
    PROXY_PORT = 8080

    HOME_URL = 'http://weibo.com/5579712614/home'



    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd

    #获取代理的browser(会打开火狐浏览器)
    def get_proxy_browser(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("network.proxy.type", 1)
        fp.set_preference("network.proxy.http",self.PROXY_HOST)
        fp.set_preference("network.proxy.http_port",self.PROXY_PORT)
        fp.set_preference("general.useragent.override","whater_useragent")
        fp.update_preferences()
        self.browser =  webdriver.Firefox(firefox_profile=fp)

    def get_chrome(self):
        chromedriver = 'G:/lessUsedTools/browser/chrome/chromedriver.exe'

        #browser = webdriver.FirefoxProfile(firefox_binary=binary)
        self.browser = webdriver.Chrome(chromedriver)

    def get_browser(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            #"Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
            #"Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
            #"Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4"
            )
        self.browser = webdriver.PhantomJS(desired_capabilities=dcap)


    #
    def login(self):
        print '开始登录'
        PORTAL_URL = 'http://m.weibo.cn'
        self.browser.get(PORTAL_URL)
        login_button_box = self.browser.find_element_by_class_name('action')
        login_button = login_button_box.find_elements_by_tag_name('a')[1]
        login_button.click()
        time.sleep(5)
        self.input_login_info()

    #登陆
    def input_login_info(self):
        username_driver = self.browser.find_element_by_id('loginName')
        username_driver.send_keys(self.username)
        passwd_driver = self.browser.find_element_by_id('loginPassword')
        passwd_driver.send_keys(self.passwd)
        submit_box = self.browser.find_element_by_id('loginAction')
        submit_box.click()
        time.sleep(5)
        self.browser.get(self.HOME_URL)
        time.sleep(5)


    #获得weibo列表
    def get_list(self):
        xpath = "//div[@class='WB_cardwrap WB_feed_type S_bg2']"
        list = self.browser.find_elements_by_xpath(xpath)
        return list

    def send_weibo(self, weibo):
       # xpath = "//span[@class='line S_line1']"
        #sendButton = weibo.find_element_by_xpath(xpath)
        sendButton = weibo.find_elements_by_class_name('pos')[1]
        sendButton.click()
        time.sleep(3)
        clickBox_xpath = "//div[@class='p_opt clearfix']"
        clickBox = weibo.find_element_by_xpath(clickBox_xpath)
        a_tags = clickBox.find_elements_by_tag_name('a')
        time.sleep(3)
        a_tags[1].click()
        print '11'

    #从微博list中的对象获取微博信息
    def get_weibo_info(self, weibo):
        title = weibo.find_element_by_class_name('WB_info').text
        print title


if __name__ == '__main__':
    weibo = WeiBoCrawler('@qq.com', '')
    weibo.get_browser()
    weibo.login()
    time.sleep(7)
    list = weibo.get_list()
    weibo.send_weibo(list[3])
