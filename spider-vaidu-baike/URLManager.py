# coding:utf-8


class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        '''
        判断是否有未爬取的URL
        :return:
        '''
        return self.new_urls_size() != 0

    def get_new_url(self):
        '''
        获取一个未爬取的URL
        :return:
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        '''
        将新的URL添加到未爬取的URL集合中
        :param url:单个URL
        :return:
        '''
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        '''
        将新的URL添加到未爬取的URL集合中
        :param urls:url 集合
        :return:
        '''
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_urls_size(self):
        '''
        获取未爬取URL集合的大小
        :return:
        '''
        return len(self.new_urls)

    def old_urls_size(self):
        '''
        获取已经爬取URL集合的大小
        :return:
        '''
        return len(self.old_urls)
