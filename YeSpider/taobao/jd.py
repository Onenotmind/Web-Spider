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
        browser.get('https://www.jd.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#key"))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search > div > div.form > button")))
        input.send_keys(q)
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > em:nth-child(1) > b")))
        get_products(browser,wait)
        return total.text
    except TimeoutException:
        search(q, browser, wait)

def next_page(page_number, browser, wait):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > input"))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > a")))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#J_bottomPage > span.p-num > a.curr"), str(page_number)))
        get_products(browser,wait)
    except TimeoutException:
        next_page(page_number, browser, wait)

def get_products(browser,wait):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#J_main .ml-wrap #J_goodsList .gl-warp .gl-item")))
    html = browser.page_source
    doc = pq(html)
    items = doc('#J_main .ml-wrap #J_goodsList .gl-warp .gl-item').items()
    for item in items:
        if(item.attr('data-sku')):
            title = item.find('.p-name').text().encode('utf-8')
            image = item.find('.err-product').attr('src')
            price = item.find('.p-price').text().encode('utf-8')
            # dealTemp = item.find('.deal-cnt').text()[:-3]
            # deal = int(dealTemp)
            shop = item.find('.p-shop').text().encode('utf-8')
            # location = item.find('.location').text().encode('utf-8')
            product = {
                'image': image,
                'price': price,
                # 'deal': deal,
                'title': title,
                'shop': shop,
                # 'location': location

            }
            save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE_JD].insert(result):
            print("success")
    except Exception:
        print(result)

def jd_test_search(q):
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver"
    browser = webdriver.Chrome(chromedriver)
    wait = WebDriverWait(browser, 10)
    total = search(q,browser,wait)
    total = int(re.compile('(\d+)').search(total).group(1))
    for i in range(2, 21):
        next_page(i,browser,wait)

# jd_test_search(u'充电宝')
