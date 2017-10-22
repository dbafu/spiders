from time import sleep

import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
import re
from pyquery import PyQuery as pq
from config_tb import *

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 10)

browser.set_window_size(1400, 900)

def search():
    print('正在搜索.....')
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        if input:
            print('find input...')
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        if submit:
            print('find submit...')
        input.send_keys(KEYWORD)
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    print('正在翻页..... : ', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager .form input"))
        )
        if input:
            print('find next input...')
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager .form span.btn.J_Submit"))
        )
        if submit:
            print('find next submit... :' + str(page_number))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
        sleep(10)
    except TimeoutException:
        return next_page(page_number)

def get_products():
    print('running get product...')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_itemlistCont')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': 'https' + item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shopname').text(),
            'location': item.find('.location').text()
        }
        if product:
            save_to_mongo(product)
        else:
            print('error accur...')

def save_to_mongo(product):
    try:
        if db[MONGO_TABLE].insert(product):
            print('存储到MongoDB成功', '\n', product)
            return True
        return False
    except Exception:
        print('存储到MongoDB错误', '\n', product)


def main():
    try:
        total = search()
        total = int(re.compile(r'(?s)(\d+)').search(total).group(1))
        for i in range(2, total + 1):
            next_page(i)
    except Exception:
        print(' main 出错了，，，')
    finally:
        browser.close()

if __name__ == '__main__':
    main()
