#coding=utf-8
__author__ = 'junyu'
import urllib2
class RequestCore:
    @staticmethod
    def request(url, charset):
        if str(url).find("http://") == -1:
            url="http://" + url
        headers={"User-Agent":"Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        req = urllib2.Request(url,headers=headers)
        response= urllib2.urlopen(req)
        html = response.read()
        html = html.decode(charset,'ignore')
        return html

    @staticmethod
    def img_request(url):
        if str(url).find("http://") == -1:
            url="http://" + url
        headers={"User-Agent":"Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        req = urllib2.Request(url,headers=headers)
        response= urllib2.urlopen(req)
        img = response.read()
        return img

    #拼装地址
    @staticmethod
    def getRealUrl(url, host):
        if str(url).find("http://") == -1:
            url = RequestCore.getWebRootPath(host) + url
            return url
        return url

    #获取网站的根路径
    @staticmethod
    def getWebRootPath(url):
        index = url.find('.com')
        return url[0:index+4]
