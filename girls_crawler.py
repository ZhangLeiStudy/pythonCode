#!/usr/local/bin python
# encoding: utf-8
# from selenium.webdriver.common.by import By
from selenium import webdriver
import unittest
import os
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# class WebKitFeatureStatusTest(unittest.TestCase):
#     def test_feature_status_page_search(self):
#         self.driver.get("https://webkit.org/status/")
# opts = webdriver.ChromeOptions()
# print opts
# str = '/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome'
# print str
# dir = os.path.join(str, '')
# print dir
# opts.binary_location()
# browser = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver', chrome_options=opts)

#
# browser = webdriver.Chrome(port=9515, chrome_options=opts)
# browser.get('https://www.baidu.com')

# class test():
#     def __init__(self):
#         self._browser = webdriver.Safari()
#         self._browser.get("http://www.baidu.com")
#
#     def get_title(self):
#         print self._browser.title
#         self._browser.quit()  #最开始没写这句，以为不会有影响导致我跌进下面的坑
#
#
# t = test()
# t.get_title()
def main():
    opts = webdriver.ChromeOptions()
#     opts.binary_location('/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome')
#   directly write location in origin code of chromeoption.init for it didn't work on my computer
    driver = webdriver.Chrome(chrome_options=opts)
    driver.get("https://www.zhihu.com/question/28481779")

    def execute_times(times):
        for i in range(times + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            try:
                driver.find_element_by_css_selector('button.QuestionMainAction').click()
                print "page" + str(i)
                time.sleep(1)
            except:
                break

    execute_times(5)

    result_raw = driver.page_source
    result_soup = BeautifulSoup(result_raw, 'html.parser')

    result_bf = result_soup.prettify()

    with open("/Users/zhanglei/crawler/zhihu/raw_result.txt", 'w') as girls:
        girls.write(result_bf)

    print 'store raw data successfully!'

    with open("/Users/zhanglei/crawler/zhihu/noscript_meta.txt", 'w') as noscript_meta:
        noscript_nodes = result_soup.find_all('noscript')
        noscript_inner_all = ""
        for noscript in noscript_nodes:
            noscript_inner = noscript.get_text()
            noscript_inner_all += noscript_inner + '\n'

        h = HTMLParser()
        noscript_all = h.unescape(noscript_inner_all)
        noscript_meta.write(noscript_all)

    print 'store noscript meta data successfully!'


    img_soup = BeautifulSoup(noscript_all, 'html.parser')
    img_nodes = img_soup.find_all('img')
    with open("/Users/zhanglei/crawler/zhihu/img_meta.txt", 'w') as img_meta:
        count = 0
        for img in img_nodes:
            if img.get('src') is not None:
                img_url = img.get('src')

                line = str(count) + "\t" + img_url + "\n"
                img_meta.write(line)
                urllib.urlretrieve(img_url, "/Users/zhanglei/crawler/zhihu/image/" + str(count) + ".jpg")
                count += 1

    print 'store meta data and image successfully!'

if __name__ == '__main__':
    main()

