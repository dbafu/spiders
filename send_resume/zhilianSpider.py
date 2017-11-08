# coding: utf-8

import re
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


username = '189******16'  # 智联账号  我的智联账号也是手机号
password = '******'  # 智联账号密码   密码故意写错，防止你登陆我账号

Job_KeyWord = '前台'  # 职位关键词
Job_Location = '北京'  # 职位所在城市

job_apply_nums = 0  # 申请计数器
starttime = datetime.datetime.now()

driver = webdriver.Chrome()

login_url = 'https://www.zhaopin.com'
job_salary_start_pa = re.compile(r'(\d+)-\d')


def login(url, username, password):
    global driver
    driver.get(url)
    time.sleep(5)
    name = driver.find_element_by_id('loginname')
    name.clear()
    name.send_keys(username)
    pw = driver.find_element_by_id('password')
    pw.clear()
    pw.send_keys(password)
    try:
        pw.send_keys(Keys.RETURN)
        time.sleep(3)
    except Exception as e:
        al = driver.switch_to_alert()
        al.accept()


def apply_job(url):
    global driver
    global job_apply_nums
    global starttime

    driver.get(url)
    time.sleep(10)
    all_jobs_xpath = '//div[@id="newlist_list_content_table"]/table'
    total_job = driver.find_elements_by_xpath(all_jobs_xpath)
    total_job_num = len(total_job)
    print(total_job_num)

    i = 2
    while i < total_job_num:
        job_checkbox_xpath = '//*[@id="newlist_list_content_table"]/table[{0}]/tbody/tr[1]/td[1]/input'.format(
            i)
        job_salary_xpath = '//div[@id="newlist_list_content_table"]/table[{0}]//td[4]'.format(
            i)
        print('job_checkbox_xpath : %s' % job_checkbox_xpath)
        print('job_salary_xpath : %s' % job_salary_xpath)
        i += 1
        j = 0
        try:
            job_checkbox = driver.find_element_by_xpath(job_checkbox_xpath)
            job_salary_pre = driver.find_element_by_xpath(
                job_salary_xpath).text
            print(job_salary_pre)
            job_salary = job_salary_start_pa.search(job_salary_pre)
            if not job_salary:
                print('工资面议忽略。。。')
                continue
            else:
                salary = int(job_salary.group(1))
                print('salary : %s' % salary)
                if salary >= 5000:
                    job_checkbox.click()
                    job_apply_nums += 1
                    j += 1
            apply_btn_xpath = '//*[@id="newlist_list_div"]/p[1]/a[1]'
        except Exception as e:
            try:
                print(e)
                al = driver.switch_to_alert()
                if al:
                    al.accept()
                else:
                    pass
            except Exception as ee:
                print(ee)
    apply_btn = driver.find_element_by_xpath(apply_btn_xpath)
    apply_btn.click()
    print('在本页共申请了 %s 个职位' % j)
    print('总共申请了 %s 个职位..' % job_apply_nums)
    endtime = datetime.datetime.now()
    print('程序运行时间 : ' + str((endtime - starttime).seconds) + ' 秒')


def main():
    global driver

    login(login_url, username, password)
    PageNum = 1
    while PageNum < 256:
        print('当前页是 ： 第 %s 页   。。。' % PageNum)
        apply_job_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl={0}&kw={1}&p={2}'
        url = apply_job_url.format(Job_Location, Job_KeyWord, PageNum)
        print(url)
        apply_job(url)
        time.sleep(5)
        PageNum += 1
        time.sleep(5)

if __name__ == '__main__':
    main()
    print('总共申请了 %s 个职位..' % job_apply_nums)
