#encoding=utf-8
class WordInfo:
    def __init__(self, word, url):
        self.word = word
        self.num = 1
        self.url_list = set()   #携带有爬虫id，url为www.xxxxx.com|12
        self.url_list.add(url)
