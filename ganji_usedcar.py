import requests
from bs4 import BeautifulSoup
import codecs
from selenium import webdriver
import time
import re
from urllib import request


def contents_url(url):
    """
    Pretend to use Chrome Inspector to identify sections of the webpage to beat 'clike-on' button
    :param url: target url
    :return: a html file
    """
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    option.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    option.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    option.add_argument('--headless') # 不弹出浏览器

    browser = webdriver.Chrome(chrome_options=option) # 新建Chrome对象
    browser.get(url)

    browser.find_element_by_class_name('detail_tel_400_outer').click() # 模拟器模拟点击
    time.sleep(1) # 根据网络情况，等待html显示手机号
    html = browser.page_source

    return(html)

def get_html(url):
    """
    To avoid of any other characters in url, transform them into utf-8
    :param url: target url
    :return: html text file
    """
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text

    except:
        return 'ERROR1'

def get_contents(url):
    """
    Anatomy html and get the information we want
    :param url: url that with user's infor
    :return: a dict of the infor
    """
    html = contents_url(url)
    soup = BeautifulSoup(html, 'lxml')

    contents = {}


    try:
        contents['title'] = soup.title.text.strip()
        contents['tel'] = soup.find_all('div', class_='detail_tel_400_text click_change_div')[0].contents[0]
        ppl = soup.find_all('p', class_='v-p2')[0].contents[1].strip()
        ppl = re.sub(' ', '', ppl)
        contents['ppl'] = ppl
        price = soup.find_all('span', class_='sp')[0].contents[0].contents[0] + \
                soup.find_all('span', class_='sp')[0].contents[1]
        contents['price'] = price

        return(contents)
    except:
        print('ERROR2')

def get_links(soup):
    """
    Get target links from the searched page
    :param soup: a bowl of beautiful soup
    :return:  a list of target links
    """

    tags = soup.find_all('a', class_='infor-title pt_tit js-title')

    if tags is None:
        return tags
    links = []

    for link in tags:
        # print(link['href'])
        links.append(link['href'])

    return links


def Out2File(contents: dict):
    """
    Write our as a CSV file separated by semi-colons.
    :param contents:  a dict contains user information
    :return:
    """
    with codecs.open('Ganji_uc.csv', 'a', encoding='utf-8') as f:
        f.write('{}; {}; {}; {}\n'.format(contents['title'], contents['price'], contents['ppl'], contents['tel']))
        f.close()

def areas():
    """

    :return:
    """
    # 北京    广州    上海    天津    深圳    重庆    南京    武汉    成都    西安    郑州    大连    苏州    济南    青岛
    # 哈尔滨    杭州    宁波    厦门    沈阳    东莞    长春    长沙      太原       南宁    石家庄
    areas = ['sh', 'tj', 'sz', 'cq', 'nj', 'wh','cd', 'xa', 'zz',\
             'dl', 'sz', 'jn', 'qd','hrb', 'hz', 'nb', 'xm', 'sy', 'dg', 'cc', 'cs', 'ty', 'nn', 'sjz']

    for area in areas:
        i = 1
        while(True):

            link = 'http://{}.ganji.com/ershouche/a1b25e999o{}/'.format(area, i)
            req = request.Request(link)
            # 传入headers， 随机IP信息
            req.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36')
            # 传入创建好的Request对象
            response = request.urlopen(req) 
            # 读取响应信息并解码
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html)
            
            judge = soup.find_all('div', class_='no-search') #查看是否还有下一页
            verifi = soup.find_all('div', class_='pop') # 查看是否为验证页面
            if judge: #没有下一页，推出
                break
            elif verifi: # 网页需要身份验证，退出
                print(area, i)
                break
            print(link)
            # time.sleep(10)
            links = get_links(soup)
            print(links)
            for link in links:
                contents = get_contents(link)
                Out2File(contents)
                print(contents)
            #time.sleep(40)
            i += 1



if __name__ == "__main__":
    areas()


# http://bj.ganji.com/ershouche/3467239543x.htm