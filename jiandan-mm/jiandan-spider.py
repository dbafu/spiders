import re
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from PIL import Image
from io import BytesIO

cap = dict(DesiredCapabilities.PHANTOMJS)
cap["phantomjs.page.settings.resourceTimeout"] = 1000
cap["phantomjs.page.settings.loadImages"] = True
cap["phantomjs.page.settings.disk-cache"] = True

cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",


driver = webdriver.PhantomJS(desired_capabilities=cap)

img_count = 0
def get_img(url, referer, host, filename):
    global img_count
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        'Host': host,
        'Referer': referer
      }
    print('正在下载图片：', url)
    img = requests.get(url, headers = headers)
    img = Image.open(BytesIO(img.content))
    img.save(filename)
    img_count += 1
    print('下载了', img_count, '张图片')

img_pattern = re.compile(r'(?s);"><a href="(.*?)".*?view_img_link">')

folder = "ooxx"
if not os.path.exists(folder):
  os.mkdir(folder)
os.chdir(folder)

urls = ["http://jandan.net/ooxx/page-{}#comments".format(str(i)) for i in range(208, 391)]


for url in urls:
    print('正在下载页面：', url)
    driver.get(url)
    referer = url.split('#')[-2]
    response = driver.page_source
    img_urls = img_pattern.findall(response)
    if len(img_urls) > 0:
        for img_url in img_urls:
            filename = img_url.split('/')[-1]
            img_host = img_url.split('/')[2]
            print('正在下载:', filename, '.....')
            url = 'http:' + img_url
            get_img(url, referer, img_host, filename)


driver.close()
