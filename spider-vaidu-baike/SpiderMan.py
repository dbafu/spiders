# coding:utf-8
from DataOutput import DataOutput
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from URLManager import UrlManager


class SpiderMan(object):

    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        # 添加入口
        self.manager.add_new_url(root_url)
        while(self.manager.has_new_url() and
              self.manager.old_urls_size() < 100):
            try:
                new_url = self.manager.get_new_url()
                # print(new_url, '.......')
                html = self.downloader.download(new_url)
                # print(html)
                new_urls, data = self.parser.parse(new_url, html)
                self.manager.add_new_urls(new_urls)
                self.output.store_data(data)
                print('已经抓取 %s 个链接' % self.manager.old_urls_size())
            except Exception as e:
                print(e)
                # print('crawl failed')
        self.output.output_html()


if __name__ == '__main__':
    spider_man = SpiderMan()
    spider_man.crawl('http://baike.baidu.com/view/284853.htm')
