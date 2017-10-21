import os
import pymongo
import requests, re, json
from urllib.parse import urlencode
from hashlib import md5
from multiprocessing import Pool
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError
from config import *

#如果系统为macOS High Sierra，该代码无法直接在pycharm里面运行，
# 需要在终端里面运行下面的命令
#export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
#然后执行python3 toutiao_spider.py
#需要在运行爬虫之前执行 mongod -dbpath ./data  运行MongoDB服务

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    header = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    response = requests.get(url, headers = header)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('请求索引页出错。。。')
        return None

def download_image(url):
    print('正在下载', url)
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    response = requests.get(url, headers=header)
    try:
        if response.status_code == 200:
            print('请求图片成功。。。。')
            save_image(response.content)
        return None
    except ConnectionError:
        print('下载图片出错。。。')
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

def get_page_detail(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    response = requests.get(url, headers=header)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('请求详情页出错 : ', url)
        return None

def parse_page_detail(html, url):
    result = re.search(r'(?s)<title>(.*?)</title>', html)
    title = result.group(1) if result else ''
    images_pattern = re.compile(r'(?s)gallery:\s(.*?)\s*?siblingList')
    result = images_pattern.search(html)
    if result:
        data = json.loads(result.group(1).rstrip(','))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images: download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False

def main(offset):
    text = get_page_index(offset, KEYWORD)
    urls = parse_page_index(text)
    for url in urls:
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            if result: save_to_mongo(result)


if __name__ == '__main__':
    groups = [x*20 for x in range(GROUP_START, GROUP_END + 1)]
    # for i in groups:
    #     main(i)

    pool = Pool()
    pool.map(main, groups)
    pool.close()
    pool.join()

