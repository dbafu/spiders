# -*- coding: utf-8 -*-

import requests
from PIL import Image
from io import BytesIO
import time
import re
import scrapy
import urllib.parse

count = 0

class jdSpider(scrapy.Spider):
	name = 'jdtopgoods'

	def start_requests(self):
		header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
		kw = urllib.parse.quote('裤子')
		for page in range(1, 5):
			page_t = page * 2 - 1
			s = (page - 1) * 30 + 1
			search_url = f'https://search.jd.com/s_new.php?keyword={kw}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={kw}&psort=3&page={page_t}&s={s}&click=0'.format()
			header['Referer'] = search_url.replace('s_new.php', 'Search')
			request = scrapy.Request(search_url, headers = header, callback = self.parse)
			request.meta['kw'] = kw
			request.meta['page'] = page
			request.meta['s'] = s
			request.meta['header'] = header
			yield request

	def parse(self, response):
		ma = response.meta
		kw = ma['kw']
		page_new = ma['page'] * 2
		s_new = ma['s'] + 30
		header = ma['header']

		pid = ','.join(response.xpath('//li[@class="gl-item"]/@data-pid').extract())
		self.get_img(response, ma)
		time.sleep(15)

		s_new_url = f'https://search.jd.com/s_new.php?keyword={kw}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={kw}&psort=3&page={page_new}&s={s_new}&scrolling=y&tpl=3_L&show_items={pid}'.format()

		req = scrapy.Request(s_new_url, headers = header, callback = self.parse_new)
		req.meta['header'] = header
		yield req

	def parse_new(self, response):
		ma = response.meta
		self.get_img(response, ma)
		time.sleep(15)


	def get_img(self, response, ma):

		global count
		img_names_debug = set()
		img_urls_debug = set()
		lis = response.xpath('//li[@class="gl-item"]')
		for li in lis:
			img_name_pre1 = li.xpath('./div[1]/div[4]/a/em')
			img_name_pre2 = img_name_pre1.xpath('string(.)').extract()[0]
			img_name = self.img_name_p(img_name_pre2)

			img_urls_pre = li.xpath('.//li[@class="ps-item"]/a/img').re(r'src="//(.*?)"|data-lazy-img="//(.*?)"')
			i_urls = [url for url in img_urls_pre if url != '']
			img_urls = list(map(self.url_p, i_urls))
			j = 0
			for img_url in img_urls:
				try:
					header = ma['header']
					img = Image.open(BytesIO(requests.get(img_url, headers = header).content))
					j += 1
					count += 1
					if img.mode is 'RGB':
						pic_name = img_name + '_' + str(j) + '_' + str(count) + '.jpg'
						img.save(pic_name)
					else:
						pic_name = img_name + '_' + str(j) + '_' + str(count) + '.png'
						img.save(pic_name)
					img_names_debug.add(pic_name)
					img_urls_debug.add(img_url)

				except Exception as e:
					print(e)
					raise e
				finally:
					print(f' <<<------debug--{j}---')

		print('num of img img_name :', len(img_names_debug))
		print('num of img img_url :', len(img_urls_debug))
		print(count)

	def img_name_p(self, name):
		name_pa = re.compile(r'[|\/\+=].*')
		img_name = name_pa.sub('_',name)
		return img_name

	def url_p(self, src):
		url = src.replace(r'/n9', r'/n8')
		return ('https:' + '//' +url)













