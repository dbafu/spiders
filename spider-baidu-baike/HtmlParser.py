# coding:utf-8

import re
from urllib.parse import urljoin


class HtmlParser(object):
    def parse(self, page_url, html_cont):
        '''
        用于解析网页的内容，抽取URL和数据
        :param page_url: 下载页面的 URL
        :param html_cont: 下载的网页的内容
        :return: 返回URL和数据
        '''
        if page_url is None or html_cont is None:
            return
        new_urls = self._get_new_urls(page_url, html_cont)
        new_data = self._get_new_data(page_url, html_cont)
        return new_urls, new_data

    def _get_new_urls(self, page_url, html_cont):
        '''
        抽取新的URL集合
        :param page_url: 下载页面的 URL
        :param soup: 下载的网页的内容，即页面源码
        :return: 返回新的 URL 集合
        '''
        new_urls = set()
        links = re.findall(
            r'(?s)<a target=.?_blank.? href="(/item/.*?)".*?>', html_cont)
        if links is None:
            return None
        for link in links:
            new_full_url = urljoin(page_url, link)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, html_cont):
        '''
        抽取有效数据
        :param page_url: 下载页面的 URL
        :param soup:
        :return:返回有效数据
        '''
        data = {}
        data['url'] = page_url
        title = re.search(r'(?s)<dd class="lemmaWgt-lemmaTitle-title">.*?'
            '<h1.*?>(.*?)</h1>', html_cont)
        if title:
            data['title'] = title.group(1)
        summary = re.search(r'(?s)<div class="lemma-summary".*?'
                            '</div>.*?</div>', html_cont)
        if summary:
            summary = summary.group()
            data['summary'] = re.sub(r'(?s)<.*?>|\n|\r', '', summary)
        if data:
            return data
