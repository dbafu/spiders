# coding: utf-8

import requests
import re
import time


url = 'http://seputu.com'
mulus_pa = re.compile(r'(?s)<div class="mulu">(.*?)</ul>')

book_title_pa = re.compile(r'(?s)<h\d>(.*?)</h\d>')
ch_link_title_pa = re.compile(r'(?s)<li><a href="(.*?)" title="(.*?)">')

body_pa = re.compile(r'[\w\W]*<!-- 自适应 -->')
ch_h1_pa = re.compile(r'<h1>([\w\W])*?</h1>')


def get_html(url):
    useragent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': useragent}
    try:
        # time.sleep(5)
        print('正在下载：', url)
        r = requests.get(url, headers=headers, timeout=None)
        if r.status_code == requests.codes.ok:
            print('下载成功 ！ : %s' % url)
            r.encoding = 'utf-8'
            html = r.text
            return html, r.url
        else:
            print('下载出错了' + ' : ' + url)
            print('status_code : ', r.status_code)
    except Exception as e:
        print('status_code : ', r.status_code)
        print(e)
        print('出现异常，重试中。。。' + ' : ' + url)
        return get_html(url)


h1_pa = re.compile(r'(?s)<h1>(.*?)</h1>')
txt2_pa = re.compile(r'(?s).*<!-- 自适应 -->')
txt3_pa = re.compile(r'(?s).*?<!-- 自适应 -->')
txt4_pa = re.compile(r'(?s).*?</script>')
txt5_pa = re.compile(
    r'(?s)<.*?>|&nbsp;|&hellip;|&ldquo;|&rdquo;|www.seputu.com|http://seputu.com/')


def get_ch_text(ch_html):
    print('\n' + '*' * 20 + ' ：正在清洗数据。。。')
    try:
        h1 = h1_pa.search(ch_html[0]).group(1)
        txt2 = txt2_pa.search(ch_html[0]).group()
        txt3 = txt3_pa.sub('', txt2, 2)
        txt4 = txt4_pa.sub('', txt3, 1)
        txt5 = txt5_pa.sub('', txt4)
        txt6 = txt5.strip() + '\n\n'
        return h1, txt6
    except Exception as e:
        print('清洗数据出现了异常,跳过该章节。。。。 : %s' % ch_html[1])
        print(e)
        pass


def save_to_file(h1_text):
    if h1_text[0]:
        ch_h1 = h1_text[0]
    else:
        ch_h1 = None
        print('章节标题获取失败。。。')
    if h1_text[1]:
        ch_text = h1_text[1]
    else:
        ch_text = None
        print('章节文本获取失败。。。')
    with open('daomu_note.txt', 'a') as f:
        f.write(ch_h1)
        f.write(ch_text)


url = 'http://seputu.com/'
html = get_html(url)
if html:
    mulus = mulus_pa.findall(html[0])
    for mulu in mulus:
        book_title = book_title_pa.search(mulu).group(1)
        ch_link_titles = ch_link_title_pa.findall(mulu)
        if ch_link_titles:
            for ch_link_title in ch_link_titles:
                title = ch_link_title[1]
                link = ch_link_title[0]
                print(title + '< : >' + link)
                ch_html = get_html(link)
                h1_text = get_ch_text(ch_html)
                save_to_file(h1_text)
