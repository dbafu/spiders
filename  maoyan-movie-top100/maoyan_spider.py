import requests, re, json
from multiprocessing import Pool
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        header = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
        #不添加UA 会被封禁
        response = requests.get(url, headers = header)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(r'(?s)<dd>.*?board-index-(.*?)".*?data-src="(.*?)"\salt="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?teger">(.*?)</i>.*?fraction">(.*?)</i>')
    print(html)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index' : item[0],
            'image' : item[1],
            'title' : item[2],
            'actor' : item[3].strip()[3:],
            'time' : item[4].strip()[5:],
            'score' : item[5] + item[6]
        }
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    # for i in range(10):
    #     main(i * 10)
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])




