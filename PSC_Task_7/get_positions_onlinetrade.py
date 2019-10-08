from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from pymongo import MongoClient

try:
    client = MongoClient('localhost', 27017)
    db = client.PSC_7
    collection = db['onlinetrade_hits']
    collection.delete_many({})
except Exception as e:
    print('Unable connect to Mongo', e)

link = 'https://www.onlinetrade.ru'
driver = webdriver.Chrome()
driver.get(link)
assert "ОНЛАЙН ТРЕЙД.РУ" in driver.title


button = driver.find_element_by_xpath('//div[@id="tabs_hits"]//span[contains(@class,"swiper-button-next")]')
is_disabled = button.get_attribute("aria-disabled")

# while is_disabled == "false":
#     time.sleep(1)
#     button.click()
#     is_disabled = button.get_attribute("aria-disabled")

goods = driver.find_elements_by_xpath('//div[@id="tabs_hits"]//div[contains(@class,"swiper-slide indexGoods__item")]')
# print('len is', len(goods))
goods_data = []

for good in goods:

    WebDriverWait(good, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'indexGoods__item__name'))
    )

    item_name = good.find_element_by_class_name('indexGoods__item__name').text

    if item_name == '':
        button.click()
        time.sleep(1)
        item_name = good.find_element_by_class_name('indexGoods__item__name').text
    price = good.find_element_by_class_name('price').text[:-2].replace(' ', '')
    bonus = good.find_element_by_class_name('indexGoods__item__bonuses').text[:-2].replace(' ', '')
    link = good.find_element_by_class_name('indexGoods__item__name').get_attribute('href')

    if item_name == '':
        pass
    else:
        goods_data.append({
            'item_name': item_name,
            'price': price,
            'bonus': bonus,
            'link': link
        })

collection.insert_many(goods_data)

print("Data collection done:")
print(f'added {len(goods_data)} item(s)')

driver.quit()
