# coding:utf-8

import urllib2, re, os

def get_res(url):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel …) Gecko/20100101 Firefox/58.0'}
    req = urllib2.Request(url, headers = header)
    res = urllib2.urlopen(req).read()
    return res

def text_fmt(text):
    t = text.replace(r'<span>', '').replace(r'</span>', '').replace(r'<br/>', ' ').strip()
    # t = t.replace(r'</span>', '')
    # t = t.replace(r'<br/>', ' ')
    t = t.strip()
    return t

def parse_div(div):
    fd = div.find('查看全文')
    duanzi_text = ''
    img_name = ''

    if fd != -1 :
        href = re.search(r'(/article/\d*?)"', div).group(1)
        c_url = 'https://www.qiushibaike.com' + href
        print c_url
        res = get_res(c_url)
        div_detail = re.search(r'<div.*qiushi_tag.*>[\w\W]*?qiushi_count', res).group()
        parse_div(div_detail)
    else:
        duanzi = re.search(r'ent">([\w\W]*?)</', div).group(1)
        if duanzi:
            duanzi_text = text_fmt(duanzi)
        img_url = re.search(r'<img src="(.*?)".*糗事#', div)
        if img_url:
            img_url = 'https:' + img_url.group(1)
            img_name = img_url.split('/')[-1]
            with open(img_name, 'wb') as img:
                img.write(get_res(img_url))
    return duanzi_text, img_name


def show(i):
    url = r'https://www.qiushibaike.com/hot/page/' + str(i)
    print url
    res = get_res(url)
    if res:
        divs = re.findall(r'<div .*qiushi_tag_.*[\w\W]*?<div id="qiushi_counts', res)
        if divs is None:
            print 'divs not found error....'
        else:
            print 'divs is not empty! size : ' + str(len(divs))
            print '''
                程序运行正常
                *********************

                输入回车查看下一个糗事段子

                输入quit 退出浏览'
            '''
            for j, div in enumerate(divs, 1):
                duanzi_text, img_name = parse_div(div)
                print '************* {} ********************'.format(j)
                if img_name:
                    print 'warning found a img : ' + img_name
                    print 'opening {0} eeeeeeeeee ......'.format(img_name)
                    os.system('open {0}'.format(img_name))
                raw_inputs = str(raw_input(''))
                if raw_inputs == 'quit':
                    return
                else:
                    print '第' + str(i) + '页' + '\t第' + str(j) + '条'
                    print ''
                    if duanzi_text:
                        print duanzi_text
                        print '.....................................'
                        if img_name:
                            os.system('killall Preview')

    if (i + 1) < 10:
        show(i + 1)

if __name__ == '__main__':
    show(1)
    # os.system('rm *g')



