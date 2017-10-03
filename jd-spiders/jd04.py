# coding: utf-8

import re, requests, time
from PIL import Image
from io import BytesIO

header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

kw = '裤子'
pid = set()

page = 1
s = (page - 1) * 30 + 1
print(s)

search_url = f'https://search.jd.com/Search?keyword={kw}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={kw}&psort=3&page={page}&s={s}&click=0'

res = requests.get(search_url.format(), headers = header)
res.encoding = 'utf-8'
html = res.text
refer = res.url

p1 = r'<ul class="gl-warp clearfix" data-tpl="3">[\w\W]*<\/ul>'
pa1 = re.compile(p1)
p2 = r'<li class="gl-item".*>[\w\W]*?<\/ul>[\w\W]*?<\/li>'
pa2 = re.compile(p2)

img_ul2_pa = re.compile(r'<ul class="ps-main">[\w\W]*?<\/u')

pid_pa = re.compile(r'data-pid="(\d*?)"')
img_name_pa = re.compile(r'<a target="_blank".*>[\W]*<em>(.*?)<')
img_name_pa2 = re.compile(r'[|\/].*')
img_url_pa = re.compile(r'<img.*?data-lazy-img="(.*?)"')

def url_p(l):
    u = l
    ur = u.replace(r'/n9', r'/n8')
    return ('https:' + ur)

ul1 = pa1.findall(html)[0]
lis = pa2.findall(ul1)
for li in lis:
    pid_pre = pid_pa.search(li).group(1)
    pid.add(pid_pre)

    img_name = img_name_pa.search(li).group(1)
    img_name = img_name_pa2.sub('', img_name)
    img_ul2 = img_ul2_pa.search(li).group()
    img_url = img_url_pa.findall(img_ul2)
    j = 0
    header['Referer'] = refer
    for i in img_url:
        ii = url_p(i)
        img = Image.open(BytesIO(requests.get(ii, headers = header).content))
        if img.mode is 'RGB':
            img.save(img_name + '_' + str(j) + '.jpg')
        else:
            img.save(img_name + '_' + str(j) + '.png')
        j += 1
        print(f'<<<------debug--{j}---')

# print(len(pid))


pid = list(pid)  #set 2 list
pid = ','.join(pid) # list 2 str

header['Referer'] = refer
page += 1
s += 30
print(s)

lazy_url = f'https://search.jd.com/s_new.php?keyword={kw}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={kw}&psort=3&page={page}&s={s}&scrolling=y&tpl=3_L&show_items={pid}'

res2 = requests.get(lazy_url.format(), headers = header)
# print(res2.url)
# print(res2.text)
# print(res2.url)
lis2 = pa2.findall(res2.text)


# print(lis2)
for li in lis2:

    img_name = img_name_pa.search(li).group(1)
    img_name = img_name_pa2.sub('', img_name)
    img_ul2 = img_ul2_pa.search(li).group()
    img_url = img_url_pa.findall(img_ul2)
    j = 0
    header['Referer'] = refer
    for i in img_url:
        ii = url_p(i)
        img = Image.open(BytesIO(requests.get(ii, headers = header).content))
        if img.mode is 'RGB':
            img.save(img_name + '_' + str(j) + '.jpg')
        else:
            img.save(img_name + '_' + str(j) + '.png')
        j += 1
        print(f'------debug--{j}--->>>>>')













