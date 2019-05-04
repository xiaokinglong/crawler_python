# 爬去小说
import requests
from bs4 import BeautifulSoup
import os

# base_url
base_url = 'http://www.xbiquge.la/xiaoshuodaquan/'

# 获取全部的小说的连接
def get_all(url):
  html = requests.get('http://www.xbiquge.la/xiaoshuodaquan/').text
  soup = BeautifulSoup(html, 'lxml')
  novel_link = soup.select('#main li a')
  for index in novel_link:
    # print(index.get('href'))
    link = index.get('href')
    get_chapter_link(link)
  # print(novel_link)
  # print(html.text)


# 获取小说的章节的页面
def get_chapter_link(url):
  page_html = requests.get(url)
  # 设置编码格式
  print(page_html)
  page_html.encoding = 'utf-8'
  # print(page_html.text)
  soup = BeautifulSoup(page_html.text, 'lxml')
  # 获取小说名
  name = soup.select('#info > h1')[0].string
  #  创建文件夹
  os.mkdir('./novel/' + name)
  # 获取章节的名称
  chapter =  soup.select('#list dd a')
  for item in chapter:
    chapter_name = item.string
    print(chapter_name)
    chapter_link = 'http://www.xbiquge.la/' + item.get('href')[1:]
    # print(chapter_name)
    get_content(name, chapter_name, chapter_link)
# 获取每一个章节的内容

def get_content(name, chapter_name, url):
  res = requests.get(url)
  res.encoding = 'utf-8'
  content_html = res.text
  soup = BeautifulSoup(content_html, 'lxml')
  context = soup.select('#content')[0].get_text()
  # 将内容写入文件中
  f = open('./novel/' + name + '/' + chapter_name + '.txt', 'wb')
  f.write(bytes(context, encoding='utf-8'))
  # with open('./novel/' + name + chapter_name, 'wb') as f:
  #   f.write()
  # context_name = soup.find(class_='bookname').find('h1').string
  # print(context_name)
  # print(context)
  # print(content_html)

get_all(base_url)

