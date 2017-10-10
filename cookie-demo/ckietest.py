import urllib
import urllib2
import cookielib

def get_csrftoken(url):
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)

    response = opener.open(url)

    for item in cookie:
        if item.name == 'csrftoken':
            return item.value


def login(loginUrl, csrftoken):
    filename = 'cookie.txt'
    cookie2 = cookielib.MozillaCookieJar(filename)
    handler = urllib2.HTTPCookieProcessor(cookie2)
    opener = urllib2.build_opener(handler)
    postdata = urllib.urlencode({
                'username': '18917596316',
                'password': '666666',
                'remember': 'true',
                'csrfmiddlewaretocken': csrftoken
        })
    headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Referer':'http://www.xuetangx.com/'
            }
    request = urllib2.Request(login_url, postdata, headers)
    response = opener.open(request)
    cookie2.save(ignore_discard = True, ignore_expires = True)

def get_res(url):
    cookie = cookielib.MozillaCookieJar()
    cookie.load('cookie.txt', ignore_discard = True, ignore_expires = True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Referer':'http://www.xuetangx.com/'
            }
    req = urllib2.Request(url)
    res = opener.open(req)
    print res.read()


url = 'http://www.xuetangx.com/'
login_url = 'http://www.xuetangx.com/v2/login_ajax'

c_url = 'http://www.xuetangx.com/courses/course-v1:TsinghuaX+44100343X+2017_T2/courseware/0e1031a03a804cbd88fef4d9d752c5d8/'

csrf = get_csrftoken(url)
login(login_url, csrf)
get_res(c_url)


