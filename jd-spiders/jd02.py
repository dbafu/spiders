# coding: utf-8

import re, requests, time, urllib.parse
from PIL import Image
from io import BytesIO
import threading

p_lis_p = r'<li class="gl-item".*>[\w\W]*?<\/ul>[\w\W]*?<\/li>'
p_lis_pa = re.compile(p_lis_p)
pid_pa = re.compile(r'data-pid="(\d*?)"')
img_name_p = re.compile(r'<a target="_blank".*>[\W]*<em>(.*?)<')
img_name_pa = re.compile(r'[|\/].*')
img_ul_pa = re.compile(r'<ul class="ps-main">[\w\W]*?<\/u')
img_url_pa = re.compile(r'<img.*?data-lazy-img="(.*?)"|<img.*?src="(.*?)"')

count = 0

class jdSpider(object):
    def __init__(self, page):
        self.header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        self.kw = urllib.parse.quote('裤子')
        self.pid = ''
        self.page = page
        self.s = page * 2 - 1
        self.page_new = page * 2
        self.s_new = page * 30 + 1
        self.search_url = f'https://search.jd.com/s_new.php?keyword={self.kw}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={self.kw}&psort=3&page={self.page}&s={self.s}&click=0'.format()
        self.header['Referer']= self.search_url.replace('s_new.php', 'Search')
        self.search_new_url = ''
        self.flag = 't'

    def get_lis(self):
        flag = self.flag
        header = self.header
        if flag == 't':
            res = requests.get(self.search_url, headers = header)
            print(res.url)
            print('get top 30 <<<<------')
        elif flag == 'b':
            res = requests.get(self.search_new_url, headers = header)
            print(res.url)
            print('get bottom 30 ------>>>>')
        else:
            print('url error !!!  requests can not konw where to go')
            return
        res.encoding = 'utf-8'
        html = res.text
        lis = p_lis_pa.findall(html)

        if flag == 't':
            self.get_pid(lis)
        return lis

    def get_pid(self, lis):
        pid = set()
        for li in lis:
            pid_pre = pid_pa.search(li).group(1)
            pid.add(pid_pre)
        pid = list(pid)  #set 2 list
        self.pid = ','.join(pid) # list 2 str
        self.search_new_url = f'https://search.jd.com/s_new.php?keyword={self.kw}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={self.kw}&psort=3&page={self.page_new}&s={self.s_new}&scrolling=y&tpl=3_L&show_items={self.pid}'.format()

    def get_img(self):
        global count
        lis = self.get_lis()

        img_names_debug = set()
        img_urls_debug = set()


        for li in lis:
            img_name_pre = img_name_p.search(li).group(1)
            img_name = img_name_pa.sub('_', img_name_pre)
            img_ul = img_ul_pa.search(li).group()
            img_urls = img_url_pa.findall(img_ul)
            img_urls = [url for i in img_urls for url in i if url != '']
            j = 0
            for img_url in img_urls:
                i_url = self.url_p(img_url)

                try:
                    img = Image.open(BytesIO(requests.get(i_url, headers = self.header).content))
                    j += 1
                    count += 1
                    if img.mode is 'RGB':
                        pic_name = img_name + '_' + str(j) + '_' + str(count) + '.jpg'
                        img.save(pic_name)
                    else:
                        pic_name = img_name + '_' + str(j) + '_' + str(count) + '.png'
                        img.save(pic_name)
                    img_names_debug.add(pic_name)
                    img_urls_debug.add(i_url)

                except Exception as e:
                    print(e)
                    raise e
                finally:
                    pass
                print(count)
                j += 1
                if self.flag == 't':
                    print(f' <<<------debug--{j}---')
                    print(self.flag)
                else:
                    print(f' ------debug--{j}--->>>')
                    print(self.flag)
        print('num of img img_name :', len(img_names_debug))
        print('num of img img_url :', len(img_urls_debug))

    def url_p(self, src):
        url = src.replace(r'/n9', r'/n8')
        return ('https:' + url)

    def main(self):
        self.get_img()  # get top 30 pics
        self.flag = 'b'
        print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
        time.sleep(20)
        self.get_img()  # get bottom 30 pics
        time.sleep(20)

if __name__ == '__main__':
    threads = []
    for page in range(1, 3):
        t = threading.Thread(target = jdSpider(page).main, args = [])
        threads.append(t)

    for t in threads:
        t.start()
        t.join()
    print('总共下载了',count,'张图片')
    print('************** end **************')







