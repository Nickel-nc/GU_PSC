from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine
import sqlite3 as lite
from pprint import pprint
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

LOGIN = 'ya.nickel-nc@yandex.ru'
with open('pwd.txt', 'r', encoding='utf-8-sig') as fp:
    PASSWORD = fp.read().rstrip()

db_filename = r'yandex_mails.db'

def to_sql(data, db_name, db_filename):

    con = lite.connect(db_filename)
    data.to_sql(db_name,
             con,
             schema=None,
             if_exists='replace',
             index=True,
             index_label=None,
             chunksize=None,
             dtype=None)
    con.close()

def from_sql(db_filename, sql):
    engine = create_engine(r'sqlite:///{}'
                           .format(db_filename))

    cquery = pd.read_sql(sql, engine)
    return cquery


def wait_xpath(ref, t=10):
    result = WebDriverWait(driver, t).until(
        EC.presence_of_element_located((By.XPATH, ref))
    )
    return result

link = 'https://passport.yandex.ru/auth/welcome?origin=home_desktop_ru_text6&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fyandex.ru'
driver = webdriver.Chrome()
driver.get(link)
assert "Авторизация" in driver.title
login_field = driver.find_element_by_name('login')
login_field.send_keys(LOGIN)
login_field.send_keys(Keys.RETURN)
pwd = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'passp-field-passwd')))
pwd.send_keys(PASSWORD)
pwd.send_keys((Keys.RETURN))
inbox = wait_xpath('//span[text()="Входящие"]')
inbox.click()
wait_xpath('//div[contains(@class, "ns-view-messages-item-box")]')
assert "Входящие — Яндекс.Почта" in driver.title
mails = driver.find_elements(By.XPATH, '//div[contains(@class, "ns-view-messages-item-box")]')
data_mail = []
iter = 0
for i in range(len(mails)):
    mail = driver.find_elements(By.XPATH, '//div[contains(@class, "ns-view-messages-item-box")]')[i]

    iter += 1
    mail.click()
    mail_from = wait_xpath('//span[contains(@class, "mail-Message-Sender-Email")]').text
    mail_to = driver.find_element_by_xpath('//div[@data-email]').get_attribute('data-email')
    message_date = driver.find_element_by_xpath('//div[contains(@class, "mail-Message-Date")]').text
    mail_subject = driver.find_element_by_xpath('//div[contains(@class,"mail-Message-Toolbar-Subject")]').text
    mail_content = driver.find_element_by_class_name('mail-Message-Body-Content').text

    data_mail.append({
        'mail_from': mail_from,
        'mail_to': mail_to,
        'message_date': message_date,
        'mail_subject': mail_subject,
        'mail_content': mail_content
    })
    print(f'Обработано {iter} писем')
    driver.back()
driver.quit()

to_sql(pd.DataFrame.from_dict(data_mail), r'mails', db_filename)
df = from_sql(db_filename, """SELECT * FROM mails""")
pprint(df)
