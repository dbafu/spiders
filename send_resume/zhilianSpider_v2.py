# coding: utf-8

import re
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


USERNAME = '18917596316'  # 智联账号  我的智联账号也是手机号
PASSWORD = '123456789p'  # 智联账号密码   密码故意写错，防止你登陆我账号

Job_KeyWord = ['前台',]  # 职位关键词
Job_Location = ['北京',]  # 职位所在城市

URL = 'https://www.zhaopin.com'

class ZhaoPin_Robot(object):
    def __init__(self, login_url, username, password, job_keyword, job_location):
        self.starttime = datetime.datetime.now()
        self.endtime = None
        self.driver = webdriver.Chrome()
        self.login_url = login_url
        self.username = username
        self.password = password
        self.job_keyword = job_keyword
        self.job_location = job_location
        self.job_apply_nums = 0
        self.PageNum = 2  # 鉴于智联吐出来的数据质量问题，一个关键词限制110页 每页60条数据
        self.job_salary_start_pa = re.compile(r'(\d+)-\d')
        self.all_jobs_xpath = '//div[@id="newlist_list_content_table"]/table'
        self.job_checkbox_xpath = '//*[@id="newlist_list_content_table"]/table[{0}]/tbody/tr[1]/td[1]/input'
        self.job_salary_xpath = '//div[@id="newlist_list_content_table"]/table[{0}]//td[4]'
        self.apply_btn_xpath = '//*[@id="newlist_list_div"]/p[1]/a[1]'

    def login(self):
        self.driver.get(self.login_url)
        time.sleep(3)
        name = self.driver.find_element_by_id('loginname')
        name.clear()
        name.send_keys(self.username)
        pw = self.driver.find_element_by_id('password')
        pw.clear()
        pw.send_keys(self.password)
        try:
            pw.send_keys(Keys.RETURN)
            time.sleep(2)
        except Exception as e:
            al = self.driver.switch_to_alert()
            al.accept()

    def apply_job(self):
        for loc in self.job_location:
            for kw in self.job_keyword:
                for pn in range(1, self.PageNum + 1):
                    apply_job_url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl={0}&kw={1}&p={2}'
                    url = apply_job_url.format(loc, kw, pn)
                    self.driver.get(url)
                    time.sleep(3)
                    em = self.driver.find_element_by_css_selector('.search_yx_tj em')
                    total_job_num = int(em.text)
                    print('在该关键词', kw, '下共有符合条件职位', total_job_num, '个', ',但是我们将只取前110页数据，每页60条数据')
                    total_job = self.driver.find_elements_by_xpath(self.all_jobs_xpath)
                    total_job_num = len(total_job) # 当前页面职位数量
                    print('当前页面职位数量:', total_job_num)

                    i = 2
                    while i < total_job_num:
                        job_checkbox_xpath = self.job_checkbox_xpath.format(i)
                        job_salary_xpath = self.job_salary_xpath.format(i)
                        i += 1
                        j = 0
                        try:
                            job_checkbox = self.driver.find_element_by_xpath(job_checkbox_xpath)
                            job_salary_pre = self.driver.find_element_by_xpath(job_salary_xpath).text
                            print(job_salary_pre)
                            job_salary = self.job_salary_start_pa.search(job_salary_pre)
                            if not job_salary:
                                print('工资面议忽略。。。')
                                continue
                            else:
                                salary = int(job_salary.group(1))
                                print('salary : %s' % salary)
                                if salary >= 3000 or '万' in job_salary_pre:
                                    job_checkbox.click()
                                    self.job_apply_nums += 1
                                    j += 1
                        except Exception as e:
                            try:
                                print(e)
                                al = self.driver.switch_to_alert()
                                if al:
                                    al.accept()
                            except Exception as ee:
                                print(ee)
                    apply_btn = self.driver.find_element_by_xpath(self.apply_btn_xpath)
                    apply_btn.click()
                    time.sleep(6)
                    print('正在爬取位于', loc, ' 关键词：', kw, '相关职位', '\n当前位于第', pn, '页', '计划爬取前110页数据')
                    print('在本页共申请了 %s 个职位' % j)

        self.endtime = datetime.datetime.now()
        print('总共申请了 %s 个职位..' % self.job_apply_nums)
        print('程序运行时间 : ' + str((self.endtime - self.starttime).seconds) + ' 秒')

    def crawl(self):
        self.login()
        self.apply_job()

if __name__ == '__main__':
    zpr = ZhaoPin_Robot(URL, USERNAME, PASSWORD, Job_KeyWord, Job_Location)
    zpr.crawl()
