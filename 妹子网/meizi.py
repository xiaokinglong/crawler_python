# 爬去妹子网的图片并下载
import requests
from bs4 import BeautifulSoup
import os

# https://www.mzitu.com/
# html = requests.get('http://www.yiren34.com/se/jingpintaotu/')
base_url = 'https://www.mzitu.com/'
# 获取的页面的函数
def page(url):
  html = requests.get(url)
  if (html.status_code == 200):
    # print('获取页面成功')
    return html.text
  else:
    print('错误')

# 提取页面中的元素的函数

def page_extract(url):
  html = page(url)
  soup = BeautifulSoup(html, 'lxml')
  item_url = soup.select('#pins li > a')
  # print(len(item_url))
  for page_item in item_url:
    # print(page_item)
    # print(page_item)clear
    link = page_item.get('href')
    # print(link)
    # 获取img 的路径
    folder_name = page_item.find('img').get('alt')
    # print(folder_name)
    # 创建文件夹
    # print('./img/'+folder_name)
    os.mkdir('./img/' + folder_name)
    # print(page_item)
    children_page(link, folder_name)
    # 获取了子页面中的内容
    # print(link)
  # 获取下一页的连接
  next = soup.find(class_='next').get('href')
  # print(next)
  if (next):
    page_extract(next)

# 子页面中的函数
def children_page(url, folder_name):
  # print('2')
  children_html = requests.get(url)
  if (children_html.status_code == 200):
    # print('获取子页面的成功')
    html = BeautifulSoup(children_html.text, 'lxml')
    # 获取 img连接并下载
    img_link = html.find(class_='main-image').find('img').get('src')
    # h获取文件名
    img_name = html.find(class_='main-title').string
    # 获取的拓展名
    numbers = len(img_link) - 4
    expand_name = img_link[numbers:]
    # print(expand_name)
    # 执行下载图片
    # 图片存放的路径
    all_name = './img/'+ folder_name +'/' + img_name+expand_name
    # 下载图片
    # header 为模拟的请求头
    header = {
      'Referer': url,
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    # print(header)
    download_img(img_link, all_name, header)
    # print(all_name)
    # print(img_link)
    # 获取下一页的连接
    next_page_links = html.find(class_='pagenavi').find_all('a')
    page_length = len(next_page_links)
    page_link = next_page_links[page_length - 1].has_attr('href')
    next_name = next_page_links[page_length - 1].find('span').string
    print(next_name)
    # has_attr()
    # 判断是否获取的到下一页的连接
    if (next_name == '下一页»'):
      page_link = next_page_links[page_length - 1].get('href')
      # print(page_link)
      children_page(page_link, folder_name)
    else:
      print('出错了')
    # print(img_link)
    # print(html)
  else:
    print('获取子页面的内容失败')


# 下载图片的函数
"""
link 图片的连接
name 存放的路径
"""
def download_img(link, name, header):
  print('开始下载了-----')
  print(header)
  source = requests.get(link, headers = header).content
  # print(source.content)
  # 将图片写入本地
  with open(name, 'wb') as f:
    f.write(source)
    print('下载结束了----')

# img_link = 'https://pic.yefu365.com/uploads/s/201904/88c52415ce4a20ca.jpg'
# download_img(img_link, 'hh')
page_extract(base_url)
