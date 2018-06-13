# -*- coding:utf-8 -*-
import time

__author__ = 'youjia'
__date__ = '2018/6/12 17:34'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from bs4 import BeautifulSoup
import requests

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)


def search(url):
    print('正在搜索')
    try:
        browser.get(url)
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mhpic")))
        # 等图片加载完成时访问网页源代码
        time.sleep(3)
        GetImg(browser.page_source)

    except TimeoutException:
        return search()


def next_page(page_number):
    print('正在翻页...', page_number)
    try:
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mhpic")))
        submit.click()
        time.sleep(2)
        html = browser.page_source
        if html.find('最后一页了') == -1:
            GetImg(html)
        else:
            GetImg(html)
            print('正在跳到下一话...')
            browser.find_element_by_link_text('下一话吧').click()
            time.sleep(2)
            GetImg(browser.page_source)
    except:
        print("跳转错误...")


def GetImg(html):
    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) " \
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.27" \
                      "85.104 Safari/537.36",
        "Content-Type": "text/html;charset=utf-8"
    }
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    # print(title)
    pattern = re.compile('<div id="mhimg0">.*?<img src="(.*?)".*?</div>', re.S)
    img = re.findall(pattern, html)
    # print(img)
    # urllib.request.urlretrieve(img[0], 'E:\\PyCharmp\\PycharmProjects\\爬虫\\爬虫及算法\\image\\漫画\\海贼王\%s.jpg' % title[:-4])
    savePath = r'E:\\PyCharmp\\PycharmProjects\\爬虫\\爬虫及算法\\image\\漫画\\海贼王'
    # print(img[0], title[:-4], '下载完成')
    htm = requests.get(img[0], headers=headers)
    with open("%s\%s.jpg" % (savePath, title[:-4]), "wb") as f:
        print("Download : %s" % title[:-4])
        f.write(htm.content)


def main():
    url = 'http://manhua.fzdm.com/2/Vol_006/index_80.html'
    search(url)
    for i in range(1, 5000):
        next_page(i)


if __name__ == "__main__":
    main()
