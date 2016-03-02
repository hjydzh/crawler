#coding:utf-8
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
class WeiboCommon:

    def get_firfox(self):
        binary = FirefoxBinary('G:/lessUsedTools/browser/firefox/firefox.exe')
        browser = webdriver.Firefox(firefox_binary=binary)
        return browser

    def get_browser(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        #phantomjs_path = "G:\programeSoftwares\python2.7\Scripts\phantomjs.exe"
        phantomjs_path = "/usr/local/bin/phantomjs"
        dcap["phantomjs.page.settings.userAgent"] = (
            #"Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
            #"Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
            #"Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
            #"Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4"
            #"Mozilla/5.0 (Linux; U; Android 4.2.1; zh-CN; VOTO X2 Build/JOP40D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.8.9.457 U3/0.8.0 Mobile Safari/533.1"
            #"Mozilla/5.0 (iPhone; U; ru; CPU iPhone OS 4_2_1 like Mac OS X; ru) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5"
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.8.9.457 U3/0.8.0 Mobile Safari/533.1"
            )
        browser = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=phantomjs_path)
        #self.browser = webdriver.PhantomJS(desired_capabilities=dcap)
        browser.set_window_size(158.1, 77.8)
        return browser

    def login(self):
        #Log.init_log()
        #logging.debug('开始登录')
        print '开始登录'
        browser = self.get_firfox()
        PORTAL_URL = 'http://m.weibo.cn'
        browser.get(PORTAL_URL)
        time.sleep(4)
        #print browser.page_source
        login_button_box = browser.find_element_by_class_name('action')
        login_button = login_button_box.find_elements_by_tag_name('a')[1]
        login_button.click()
        time.sleep(5)
        self.input_login_info(browser)
        return browser

    #登陆
    def input_login_info(self, browser):
        username = browser.find_element_by_id('loginName')
        username.send_keys(' ')
        passwd = browser.find_element_by_id('loginPassword')
        passwd.send_keys(' ')
        submit_box = browser.find_element_by_id('loginAction')
        submit_box.click()
        time.sleep(5)
        browser.get('http://weibo.com')
        time.sleep(5)

