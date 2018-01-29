# -*- coding: UTF-8 -*-
import re
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]



def search(q, browser, wait):

    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")))
        input.send_keys(q)
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total")))
        get_products(browser,wait)
        return total.text
    except TimeoutException:
        search(q, browser, wait)

def next_page(page_number, browser, wait):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_number)))
        get_products(browser,wait)
    except TimeoutException:
        next_page(page_number, browser, wait)

def get_products(browser,wait):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item")))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .J_MouserOnverReq').items()
    for item in items:
        title = item.find('.title').text().encode('utf-8')
        image = item.find('.pic .img').attr('src')
        price = item.find('.price').text().encode('utf-8')
        dealTemp = item.find('.deal-cnt').text()[:-3]
        deal = int(dealTemp)
        shop = item.find('.shop').text().encode('utf-8')
        location = item.find('.location').text().encode('utf-8')
        product = {
            'image': image,
            'price': price,
            'deal': deal,
            'title': title,
            'shop': shop,
            'location': location

        }
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print("success")
    except Exception:
        print(result)

def test_search(q):
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver"
    browser = webdriver.Chrome(chromedriver)
    wait = WebDriverWait(browser, 10)
    total = search(q,browser,wait)
    total = int(re.compile('(\d+)').search(total).group(1))
    for i in range(2, 11):
        next_page(i,browser,wait)


# test_search(u"美食")

# def main(q):
#     total = search(q)
#     total = int(re.compile('(\d+)').search(total).group(1))
#     for i in range(2, total+1):
#         next_page(i)
#
#
#
# if __name__ == '__main__':
#     main(u'美食')