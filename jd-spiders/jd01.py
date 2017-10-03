# coding: utf-8

from selenium import webdriver
import time


driver = webdriver.PhantomJS()

url = 'https://www.jd.com'

driver.get(url)
js = '''
(function scrollToBottom() {

    var Height = document.body.clientHeight,  //文本高度
        screenHeight = window.innerHeight,  //屏幕高度
        INTERVAL = 100,  // 滚动动作之间的间隔时间
        delta = 500,  //每次滚动距离
        curScrollTop = 0;    //当前window.scrollTop 值

    var scroll = function () {
        curScrollTop = document.body.scrollTop;
        window.scrollTo(0,curScrollTop + delta);
    };

    var timer = setInterval(function () {
        var curHeight = curScrollTop + screenHeight;
        if (curHeight >= Height){   //滚动到页面底部时，结束滚动
            clearInterval(timer);
        }
        scroll();
    }, INTERVAL)
})();
'''
driver.execute_script(js)

time.sleep(15)
driver.save_screenshot('jd.png')
driver.quit()





