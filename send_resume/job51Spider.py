# coding: utf-8

import re
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


username = '189******16'  # 智联账号  我的智联账号也是手机号
password = '*****'  # 智联账号密码   密码故意写错，防止你登陆我账号

Job_KeyWord = '前台'  # 职位关键词
Job_Location = '北京'  # 职位所在城市

PAGE_NUM = 120

job_apply_nums = 0  # 申请计数器
starttime = datetime.datetime.now()

driver = webdriver.Chrome()

login_url = 'http://www.51job.com/'
job_salary_start_pa = re.compile(r'([\d.]+)-\d')


def login(url, username, password):
    global driver
    driver.get(url)
    time.sleep(5)
    login_btn_xpath = '/html/body/div[3]/div/div[2]/div[1]/div[3]/span[1]'
    login_btn = driver.find_element_by_xpath(login_btn_xpath)
    login_btn.click()
    time.sleep(1)

    loginname = driver.find_element_by_id('loginname')
    loginname.send_keys(username)
    time.sleep(1)
    pw = driver.find_element_by_id('password')
    pw.send_keys(password)
    pw.send_keys(Keys.RETURN)
    time.sleep(5)

    search_input = driver.find_elements_by_id('kwdselectid')[0]
    search_input.send_keys(Job_KeyWord)
    submit_btn_xpath = '/html/body/div[3]/div/div[1]/div/button'
    search_submit_btn = driver.find_element_by_xpath(submit_btn_xpath)
    search_submit_btn.click()
    url = driver.current_url
    # print(url)


def apply_job():
    global driver
    global job_apply_nums
    global starttime
    time.sleep(5)
    total_job = driver.find_elements_by_css_selector('.dw_table .el')
    total_job_num = len(total_job)
    print(total_job_num)

    i = 1
    j = 0
    while i < total_job_num:
        job_checkbox_xpath = '//*[@id="resultList"]/div[{0}]/p/em'.format(
            i + 3)
        job_salary_xpath = '//*[@id="resultList"]/div[{0}]/span[3]'.format(
            i + 3)
        print('job_checkbox_xpath : %s' % job_checkbox_xpath)
        print('job_salary_xpath : %s' % job_salary_xpath)
        i += 1

        job_checkbox = driver.find_element_by_xpath(job_checkbox_xpath)
        job_salary_pre = driver.find_element_by_xpath(job_salary_xpath).text
        print(job_salary_pre)
        job_salary = job_salary_start_pa.search(job_salary_pre)
        try:
            if not job_salary:
                print('工资面议忽略。。。')
                continue
            else:
                salary = float(job_salary.group(1))
                print('salary : %s' % salary)
                if salary >= 5.5:
                    job_checkbox.click()
                    job_apply_nums += 1
                    j += 1
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

    apply_btn_xpath = '//*[@id="resultList"]/div[2]/div[2]/span[1]'
    apply_btn = driver.find_element_by_xpath(apply_btn_xpath)
    apply_btn.click()
    if j == 0:
        al = driver.switch_to_alert()
        al.accept()
    print('在本页共申请了 %s 个职位' % j)
    print('总共申请了 %s 个职位..' % job_apply_nums)
    endtime = datetime.datetime.now()
    print('程序运行时间 : ' + str((endtime - starttime).seconds) + ' 秒')
    time.sleep(6)


def get_next_page_url():
    global driver
    cur_url = driver.current_url
    cur_p_num_pa = re.compile(r'\d+?(?=\.html)')
    cur_p_num = cur_p_num_pa.search(cur_url).group()
    print('当前在第 %s 页' % cur_p_num)
    cur_p_num = int(cur_p_num)
    next_p_num = cur_p_num + 1
    next_url = cur_p_num_pa.sub(str(next_p_num), cur_url)
    return next_url


def main():
    global driver
    login(login_url, username, password)
    i = 1
    while i < PAGE_NUM:
        driver.get(get_next_page_url())
        apply_job()
        i += 1


if __name__ == '__main__':
    main()
    print('总共申请了 %s 个职位..' % job_apply_nums)
