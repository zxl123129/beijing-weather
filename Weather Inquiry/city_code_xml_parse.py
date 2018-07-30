#coding=utf-8
import  xml.dom.minidom

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')   #   此处为确保控制台print方法能正常输出中文

def get_city_code():
    #打开xml文档
    dom = xml.dom.minidom.parse('static/api.xml')
    #得到文档元素对象
    root = dom.documentElement
    #找到指定名称的标签
    county = root.getElementsByTagName('county')
    #遍历所有城市并存储到字典dict中
    dict = {}
    for var in county:
        dict[var.getAttribute('name')] = var.getAttribute('weatherCode')
    return dict

