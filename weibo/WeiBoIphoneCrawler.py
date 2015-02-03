#coding:utf-8
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from log.Log import Log
import logging

class WeiBoCrawler:
    #代理地址
    PROXY_HOST = '10.19.110.31'

    #代理端口
    PROXY_PORT = 8080

    PORTAL_URL = 'http://m.weibo.cn'

    HOME_URL = 'http://weibo.com/52weis/home'

    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd

    def get_browser(self):
        Log.init_log()
        logging.debug('登陆')
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            #"Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
            #"Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
            #"Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
            #"Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4"
            #"Mozilla/5.0 (Linux; U; Android 4.2.1; zh-CN; VOTO X2 Build/JOP40D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.8.9.457 U3/0.8.0 Mobile Safari/533.1"
            #"Mozilla/5.0 (iPhone; U; ru; CPU iPhone OS 4_2_1 like Mac OS X; ru) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5"
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.8.9.457 U3/0.8.0 Mobile Safari/533.1"
            )
        self.browser = webdriver.PhantomJS(desired_capabilities=dcap)
        self.browser.set_window_size(158.1, 77.8)


    #
    def login(self):
        Log.init_log()
        logging.debug('微博登录开始')
        browser = self.browser
        browser.get(self.PORTAL_URL)
        time.sleep(4)
        #print browser.page_source
        login_button_box = browser.find_element_by_class_name('action')
        login_button = login_button_box.find_elements_by_tag_name('a')[1]
        login_button.click()
        time.sleep(5)
        self.input_login_info()

    #登陆
    def input_login_info(self):
        username = self.browser.find_element_by_id('loginName')
        username.send_keys(self.username)
        passwd = self.browser.find_element_by_id('loginPassword')
        passwd.send_keys(self.passwd)
        submit_box = self.browser.find_element_by_id('loginAction')
        submit_box.click()


    #获得weibo列表
    def get_list(self):
        xpath = "//div[@class='card card9 line-around']"
        list = self.browser.find_elements_by_xpath(xpath)
        return list

    def send_weibo(self, weibo):
       # xpath = "//span[@class='line S_line1']"
        #sendButton = weibo.find_element_by_xpath(xpath)
        sendButtonBox = weibo.find_element_by_tag_name('footer')
        sendButton = sendButtonBox.find_elements_by_tag_name('a')[0]
        sendButton.click()
        time.sleep(3)
        send_box = self.browser.find_element_by_id('box')
        send = send_box.find_elements_by_tag_name('a')[1]
        time.sleep(2)
        send.click()

    #从微博list中的对象获取微博信息
    def get_weibo_info(self, weibo):
        title = weibo.find_element_by_class_name('WB_info').text
        print title


if __name__ == '__main__':
    weibo = WeiBoCrawler('junyuhuangwan@sina.com', 'weibojun@123')
    weibo.get_browser()
    weibo.login()
    time.sleep(5)
    list = weibo.get_list()
    weibo.send_weibo(list[3])
