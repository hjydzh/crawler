#coding=utf-8

class HtmlTag:
    def __init__(self):
        self.tagName =  ''   #html标签的类别，如div, span等
        self.attr = ''       #标签的属性,如id, name, class
        self.attrValue = None  #属性的值
        self.order = None      #标签的顺序

