# coding: utf-8

import re
import time
import datetime
from urllib.parse import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


username = '15368666377'  # 前程无忧账号  我的智联账号也是手机号
password = '6i6ob6i870203'  # 前程无忧账号密码   密码故意写错，防止你登陆我账号

Job_KeyWords = ['化学',]
# Job_KeyWords = ['化学 检测', '化学 研究', '化学 分析', '化学 测试', '化学 研究员', '化学 科研', '化学 管理', '化学 仪器']
k_count = 1   # 关键词计数器
k_count_total = len(Job_KeyWords)

CITY = ['武汉', '郑州']
c_count = 1   # 城市计数器
c_count_total = len(CITY)

page_num_cur = 1
page_num_max = 0  # 一个关键词下的职位页数

job_apply_nums = 0  # 申请计数器
starttime = datetime.datetime.now()

driver = webdriver.Chrome()

login_url = 'http://www.51job.com/'
job_salary_start_pa = re.compile(r'([\d.]+)-\d')


def login(url, username, password):
    global driver
    global PAGE_NUM
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

    location_swith_btn = driver.find_element_by_id('work_position_input')
    location_swith_btn.click()
    time.sleep(1)
    target_location_btn = driver.find_element_by_id('work_position_click_center_right_list_category_000000_180200')
    target_location_btn.click()
    curr_location = driver.find_element_by_css_selector('.ttag em')
    curr_location.click()
    loc_save_btn = driver.find_element_by_id('work_position_click_bottom_save')
    loc_save_btn.click()


def apply_job():
    global driver
    global job_apply_nums
    global starttime
    global page_num_cur
    global page_num_max
    global k_count
    global k_count_total
    global c_count
    global c_count_total
    time.sleep(5)
    total_job = driver.find_elements_by_css_selector('.dw_table .el')
    total_job_num = len(total_job)
    if total_job_num <= 1:
        return None
    print('本页职位数目为 ： %s 个' % (total_job_num - 1))

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
                if salary >= 6 or '万' in job_salary_pre:
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
    print('当前位于第 %s 个城市，总共 %s 个城市' % (c_count, c_count_total))
    print('当前位于第 %s 个关键词下，总共 %s 个关键词' % (k_count, k_count_total))
    print('当前在第 %s 页 该关键词下 总共 %s 页' % (page_num_cur, page_num_max))
    print('在本页共申请了 %s 个职位' % j)
    print('总共申请了 %s 个职位..' % job_apply_nums)
    endtime = datetime.datetime.now()
    print('程序运行时间 : ' + str((endtime - starttime).seconds) + ' 秒')
    time.sleep(6)

def get_new_page(url):
    global driver
    global page_num_cur
    global page_num_max

    driver.get(url)
    page_num_max_text = driver.find_element_by_css_selector('.rt + .rt').text
    num = re.search(r'\/\s(\d+)', page_num_max_text).group(1)
    page_num_max = int(re.search(r'\/\s(\d+)', page_num_max_text).group(1))


location_code = {'北京': '010000', '上海': '020000', '广州': '030200', '深圳': '040000', '武汉': '180200', '西安': '200200', '杭州': '080200', '南京': '070200', '成都': '090200', '重庆': '060000', '东莞': '030800', '大连': '230300', '沈阳': '230200', '苏州': '070300', '昆明': '250200', '长沙': '190200', '合肥': '150200', '宁波': '080300', '郑州': '170200', '天津': '050000', '青岛': '120300', '济南': '120200', '哈尔滨': '220200', '长春': '240200', '福州': '110200', '乐东': '102000', '雅安': '091800', '烟台': '120400', '盐城': '071300', '延安': '200600', '延边': '241100', '延吉': '240800', '燕郊开发区': '161300', '杨凌': '201200', '扬州': '070800', '洋浦经济开发区': '100400', '阳江': '032800', '阳泉': '210800', '伊春': '220300', '伊犁': '310500', '宜宾': '090700', '宜昌': '180300', '宜春': '131000', '义乌': '081400', '益阳': '190800', '银川': '290200', '鹰潭': '130700', '营口': '230500', '永州': '191300', '榆林': '200800', '玉林': '140600', '玉树': '320900', '玉溪': '250400', '岳阳': '190600', '云浮': '032900', '运城': '210300', '枣庄': '121600', '湛江': '031700', '漳州': '110500', '张家港': '071400', '张家界': '191400', '张家口': '160900', '张掖': '270900', '昭通': '251300', '肇庆': '031800', '镇江': '071000', '中山': '030700', '中卫': '290400', '舟山': '081100', '周口': '170800', '珠海': '030500', '株洲': '190300', '驻马店': '171400', '资阳': '091400', '淄博': '120700', '自贡': '090800', '遵义': '260300', '万宁': '100700', '威海': '120600', '潍坊': '120500', '渭南': '200700', '温州': '080400', '文昌': '100500', '文山': '251400', '乌海': '281000', '乌兰察布': '281200', '乌鲁木齐': '310200', '无锡': '070400', '芜湖': '150300', '梧州': '140700', '吴忠': '290300', '武威': '270700', '五家渠': '311000', '五指山': '101000', '西昌': '091900', '西宁': '320200', '西双版纳': '251500', '锡林郭勒盟': '281400', '厦门': '110300', '仙桃': '181400', '咸宁': '181300', '咸阳': '200300', '襄阳': '180500', '湘潭': '190400', '湘西': '191500', '孝感': '180900', '新乡': '170700', '新余': '130600', '忻州': '211100', '信阳': '171200', '兴安盟': '281300', '邢台': '161100', '徐州': '071100', '许昌': '171100', '宣城': '151400', '三门峡': '171800', '三明': '110700', '三沙': '101500', '三亚': '100300', '山南': '300500', '汕头': '030400', '汕尾': '032400', '商洛': '201100', '商丘': '171300', '上饶': '131200', '韶关': '031400', '邵阳': '191000', '绍兴': '080500', '神农架': '181700', '十堰': '180600', '石河子': '310800', '石家庄': '160200', '石嘴山': '290500', '双鸭山': '221100', '朔州': '210900', '四平': '240600', '松原': '240700', '宿迁': '072000', '宿州': '151600', '随州': '181200', '绥化': '220400', '遂宁': '091500', '塔城': '311500', '台州': '080800', '泰安': '121100', '泰兴': '072300', '泰州': '071800', '太仓': '071600', '太原': '210200', '唐山': '160500', '天门': '181600', '天水': '270600', '铁岭': '231200', '通化': '240500', '通辽': '280700', '铜川': '200500', '铜陵': '150800', '铜仁': '260600', '图木舒克': '311100', '吐鲁番': '311400', '屯昌': '101200', '攀枝花': '091000', '盘锦': '231300', '萍乡': '130500', '平顶山': '171000', '平凉': '271000', '莆田': '110600', '普洱': '251100', '濮阳': '171600', '七台河': '221300', '齐齐哈尔': '220600', '黔东南': '260900', '黔南': '261000', '黔西南': '260800', '潜江': '181500', '钦州': '140900', '秦皇岛': '160600', '清远': '031900', '庆阳': '271300', '琼海': '100600', '琼中': '101600', '曲靖': '250300', '泉州': '110400', '衢州': '081200', '日喀则': '300300', '日照': '121200', '拉萨': '300200', '莱芜': '121800', '来宾': '141300', '兰州': '270200', '廊坊': '160300', '乐山': '090400', '丽江': '250600', '丽水': '081000', '连云港': '071200', '凉山': '092300', '聊城': '121700', '辽阳': '231100', '辽源': '240400', '林芝': '300400', '临沧': '251800', '临汾': '210500', '临高': '101400', '临夏': '271400', '临沂': '120800', '陵水': '102100', '柳州': '140400', '六安': '151200', '六盘水': '260400', '龙岩': '111000', '陇南': '271200', '娄底': '191200', '吕梁': '211200', '洛阳': '170300', '泸州': '090500', '漯河': '171500', '马鞍山': '150500', '茂名': '032300', '梅州': '032600', '眉山': '091200', '绵阳': '090300', '牡丹江': '220700', '那曲': '300700', '南昌': '130200', '南充': '091100', '南宁': '140200', '南平': '110800', '南通': '070900', '南阳': '170600', '内江': '090900', '宁德': '110900', '怒江': '251900', '鸡西': '220900', '吉安': '130900', '吉林': '240300', '济宁': '120900', '济源': '171900', '嘉兴': '080700', '嘉峪关': '270400', '佳木斯': '220800', '江门': '031500', '焦作': '170500', '揭阳': '032200', '金昌': '270300', '金华': '080600', '锦州': '230700', '晋城': '210700', '晋中': '211000', '荆门': '180800', '荆州': '180700', '景德镇': '130400', '靖江': '072500', '九江': '130300', '酒泉': '270500', '喀什地区': '310400', '开封': '170400', '开平': '032700', '克拉玛依': '310300', '克孜勒苏柯尔克孜': '311700', '昆山': '070600', '国外': '360000', '广东省': '030000', '江苏省': '070000', '浙江省': '080000', '四川省': '090000', '海南省': '100000', '福建省': '110000', '山东省': '120000', '江西省': '130000', '广西': '140000', '安徽省': '150000', '河北省': '160000', '河南省': '170000', '湖北省': '180000', '湖南省': '190000', '陕西省': '200000', '山西省': '210000', '黑龙江省': '220000', '辽宁省': '230000', '吉林省': '240000', '云南省': '250000', '贵州省': '260000', '甘肃省': '270000', '内蒙古': '280000', '宁夏': '290000', '西藏': '300000', '新疆': '310000', '青海省': '320000', '香港': '330000', '澳门': '340000', '台湾': '350000', '哈密': '310700', '海北': '320500', '海东': '320300', '海口': '100200', '海南': '320700', '海宁': '081600', '海西': '320400', '邯郸': '160700', '汉中': '200900', '菏泽': '121400', '和田': '311600', '河池': '141200', '河源': '032100', '鹤壁': '171700', '鹤岗': '221000', '贺州': '141500', '黑河': '221200', '衡水': '161200', '衡阳': '190500', '红河州': '251000', '呼和浩特': '280200', '呼伦贝尔': '281100', '葫芦岛': '230900', '湖州': '080900', '怀化': '191100', '淮安': '071900', '淮北': '151700', '淮南': '151100', '黄冈': '181100', '黄南': '320600', '黄山': '151000', '黄石': '180400', '惠州': '030300', '达州': '091700', '大理': '250500', '大庆': '220500', '大同': '210400', '大兴安岭': '221400', '丹东': '230800', '丹阳': '072100', '德宏': '251600', '德阳': '090600', '德州': '121300', '邓州': '172000', '迪庆': '252000', '定安': '101100', '定西': '271100', '东方': '100900', '东营': '121000', '儋州': '100800', '鄂尔多斯': '280800', '鄂州': '181000', '恩施': '181800', '防城港': '140800', '佛山': '030600', '抚顺': '230600', '抚州': '131100', '阜新': '231500', '阜阳': '150700', '甘南': '271500', '甘孜': '092100', '赣州': '130800', '固原': '290600', '广安': '091300', '广元': '091600', '桂林': '140300', '贵港': '141000', '贵阳': '260200', '果洛': '320800', '阿坝': '092200', '阿克苏': '310600', '阿拉尔': '310900', '阿拉善盟': '281500', '阿勒泰': '311300', '阿里': '300800', '鞍山': '230400', '安康': '201000', '安庆': '150400', '安顺': '260500', '安阳': '170900', '巴彦淖尔': '280900', '巴音郭楞': '311800', '巴中': '092000', '白城': '241000', '白沙': '101800', '白山': '240900', '白银': '270800', '百色': '141100', '蚌埠': '150600', '包头': '280400', '保定': '160400', '保山': '251200', '保亭': '101700', '宝鸡': '200400', '北海': '140500', '本溪': '231000', '毕节': '260700', '滨州': '121500', '博尔塔拉': '311900', '亳州': '151800', '沧州': '160800', '昌都': '300600', '昌吉': '311200', '昌江': '101900', '常德': '190700', '常熟': '070700', '常州': '070500', '长治': '210600', '朝阳': '231400', '潮州': '032000', '郴州': '190900', '澄迈': '101300', '承德': '161000', '池州': '151500', '赤峰': '280300', '崇左': '141400', '滁州': '150900', '楚雄': '251700'}


def main():
    global driver
    global page_num
    global page_num_cur
    global page_num_max
    global k_count
    global k_count_total
    global c_count
    global c_count_total

    login(login_url, username, password)

    location_codes = [location_code[city] for city in CITY]
    kws = [quote(quote(kw)) for kw in Job_KeyWords]

    for loc in location_codes:
        k_count = 1
        for kw in kws:
            page_num_cur = 1
            url = 'http://search.51job.com/list/{0},000000,0000,00,9,99,{1},2,{2}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(loc, kw, page_num_cur)
            get_new_page(url)
            while page_num_cur <= page_num_max:
                apply_job()
                page_num_cur += 1
                if page_num_cur > page_num_max:
                    break
                url = 'http://search.51job.com/list/{0},000000,0000,00,9,99,{1},2,{2}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(loc, kw, page_num_cur)
                get_new_page(url)
            k_count += 1
        c_count += 1


if __name__ == '__main__':
    main()
    print('总共申请了 %s 个职位..' % job_apply_nums)
