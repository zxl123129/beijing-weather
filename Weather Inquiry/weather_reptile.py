# coding : UTF-8

import requests #用来抓取网页的html源代码
import random   #取随机数
import time #时间相关操作 
import socket   #
import http.client  #socket和http.client在这里只用于异常处理
from bs4 import BeautifulSoup   #用来代替正则式取源码中相应标签中的内容 

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')   #   此处为确保控制台print方法能正常输出中文

def get_content(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
            rep.encoding = 'utf-8'
            break
      
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text

'''
header是requests.get的一个参数，目的是模拟浏览器访问 
header通过chrome的开发者工具获得
timeout是设定的一个超时时间，取随机数是因为防止被网站认定为网络爬虫。 
然后通过requests.get方法获取网页的源代码
rep.encoding = utf-8是将源代码的编码格式改为utf-8（不加则源代码中中文部分会为乱码） 
随后是一些异常处理 
最后返回 rep.text
'''

def get_data(html_text):
    final = [['日期', 'weather', '最高温度', '最低温度', '风向', '风速']] # 初始化表头数据
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body # 获取body部分
    data = body.find('div', {'id': '7d'})  # 找到id为7d的div
    ul = data.find('ul')  # 获取ul部分
    li = ul.find_all('li')  # 获取所有的li

    for day in li: # 对每个li标签中的内容进行遍历
        temp = []
        date = day.find('h1').string  # 找到日期
        temp.append(date)  # 添加到temp中
        inf = day.find_all('p')  # 找到li中的所有p标签
        temp.append(inf[0].string,)  # 第一个p标签中的内容（天气状况）加到temp中
        if inf[1].find('span') is None:
            temperature_highest = None # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
        else:
            temperature_highest = inf[1].find('span').string  # 找到最高温
            temperature_highest = temperature_highest.replace('℃', '')  # 到了晚上网站会变，最高温度后面也有个℃
        temperature_lowest = inf[1].find('i').string  # 找到最低温
        temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号
        temp.append(temperature_highest)   # 将最高温添加到temp中
        temp.append(temperature_lowest)   #将最低温添加到temp中
        wind = inf[2].find_all('span')
        w = ''
        for var in wind:
            w += (var.get('title')+' ')
        temp.append(w)  #   将风向添加到temp中
        speed = inf[2].find('i').string
        temp.append(speed)  #   将风速添加到temp中
        final.append(temp)   #  将temp加到final中

    return final    #   final列表包含了所有要展示的数据

'''
获取html中我们所需要的字段
这里主要要用到BeautifulSoup 
首先还是用开发者工具查看网页源码，并找到所需字段的相应位置
分析html后可知所需要字段都在 id = “7d”的“div”的ul中
日期在每个li中h1 中，天气状况在每个li的第一个p标签内
最高温度和最低温度在每个li的span和i标签中
风向在span中，风速在i标签中
'''

'''
程序入口:
'''
def get_weather_data(city_code):
    city_code = city_code   # 接受指定城市的城市代码
    url ='http://www.weather.com.cn/weather/{}.shtml'.format(city_code)    # 中国天气网指定代码城市的天气信息地址
    html = get_content(url)
    result = get_data(html)
    return result

