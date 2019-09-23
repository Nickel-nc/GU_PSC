#!/usr/bin/env python
# coding: utf-8

# ## Методы сбора и обработки данных из сети Интернет
# 
# ### Задание 2: скраппинг данных с интернет ресурсов

# In[346]:


from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
import time
from lxml import html
import random
import numpy as np
import re


# ### HH.ru

# In[404]:


position = 'Data scientist'
main_link = 'https://hh.ru'
start_link = 'https://hh.ru/search/vacancy?text=' + position.replace(' ','+') + '&page='
headers = {'User-agent': 'Chrome/76.0.3809.132'}
var_page = '0'

# Определяет кол-во страниц для парсинга
def find_max_pages_hh(start_link, var_page):
    html_page = requests.get(start_link + var_page, headers=headers).text
    parsed_html = bs(html_page, 'html.parser')
    page_bar = parsed_html.findChildren('a',{'class':'bloko-button HH-Pager-Control'})
    max_page_num = int(page_bar[len(page_bar)-1]['data-page'])
    return max_page_num  


max_page = find_max_pages_hh(start_link, var_page)


# In[405]:


data_hh = []

for i in range(max_page):
    current_html = requests.get(main_link + '/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=Data+scientist&page=' + str(i), headers=headers).text
    parsed_html = bs(current_html, 'html.parser')
    vacancy_list = parsed_html.findAll('div',{'class':'vacancy-serp-item'})
    print(f'Обработка {i+1} страницы из {max_page + 1}')

        # Парсит блоки на текущей странице
    for vacancy in vacancy_list:
        # print('.', end='')
        vacancy_number = int(vacancy.find('a',{'class':'bloko-link HH-LinkModifier'})['data-position']) # № Вакансии на сайте
        vacancy_name = vacancy.find('a',{'class':'bloko-link HH-LinkModifier'}).getText() # Наименование вакансии
        try:
            firm_name = vacancy.find('a',{'class':'bloko-link bloko-link_secondary'}).getText() # Фирма
        except:
            firm_name = None
        vacancy_link = vacancy.find('a',{'class':'bloko-link HH-LinkModifier'})['href'] # Ссылка
        salary_min = None # З.п (мин)
        salary_max = None # З.п (макс)
        salary_block = vacancy.find('div',{'class':'vacancy-serp-item__sidebar'}).getText().replace('\xa0',' ')
        if salary_block.find('от') != -1:
            salary_min = int(salary_block.split()[1] + salary_block.split()[2])
        elif salary_block.find('до') != -1:
            salary_max = int(salary_block.split()[1] + salary_block.split()[2])
        elif salary_block.find('-') != -1:
            salary_min = int((salary_block.split('-')[0]).replace(' ',''))
            salary_max = int((salary_block.split('-')[1]).split(' ')[0] + (salary_block.split('-')[1]).split(' ')[1])

        publish_date = vacancy.find('span',{'class': 'vacancy-serp-item__publication-date'}).getText().replace('\xa0',' ') # Добавляет "сырую дату актуальности"
        tasks_shrt = vacancy.find('div',{'class': 'g-user-content'}).contents[0].getText() # Краткое описание деятельности
        prereq_shrt = vacancy.find('div',{'class': 'g-user-content'}).contents[1].getText() # Краткое описание требований
        city = vacancy.find('span',{'class': 'vacancy-serp-item__meta-info'}).contents[0].replace(',','') # Город
        try:
            metro_station = vacancy.find('span',{'class': 'vacancy-serp-item__meta-info'}).contents[1].getText() # Станция метро
        except:
            metro_station = None    

        data_hh.append({
                    'vacancy_name': vacancy_name,
                    'firm_name': firm_name,
                    'vacancy_link': vacancy_link,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'publish_date': publish_date,
                    'tasks_shrt': tasks_shrt,
                    'prereq_shrt': prereq_shrt,
                    'city': city,
                    'metro_station': metro_station,
                    'site': 'hh.ru'

            })

    

    time.sleep(2 + np.random.rand())


# In[406]:


len(data_hh)


# In[407]:


ordered_cols = ['firm_name', 'vacancy_name', 'salary_min', 'salary_max',
                'city', 'metro_station', 'prereq_shrt', 'tasks_shrt', 'publish_date', 'vacancy_link', 'site']
df_hh = pd.DataFrame.from_dict(data_hh)
df_hh = df_hh[ordered_cols]


# In[408]:


df_hh.info()


# In[409]:


df_hh.head()


# ### Superjob.ru

# In[357]:


position = 'python'
main_link_sj = 'https://www.superjob.ru'
search_sj = '/vacancy/search/?keywords=' + position.replace(' ','-')
headers = {'User-agent': 'Chrome/76.0.3809.132'}

html = requests.get(main_link_sj + search_sj, headers=headers).text
parsed_html = bs(html, 'html.parser')


# In[358]:


def find_last_page(parsed_html):
    page_bar = parsed_html.find('a', {'class': 'f-test-button-1'})
    if not page_bar:
            last_page = 1
    else:
        page_bar = page_bar.findParent()
        last_page = int(page_bar.find_all('a')[-2].getText())
    return last_page

max_page = find_last_page(parsed_html)


# In[397]:


data_sj = []

for i in range(max_page):
    current_html = requests.get(main_link_sj + search_sj + '&page=' + str(i + 1), headers=headers).text
    parsed_html = bs(current_html, 'html.parser')    
    vacancy_list = parsed_html.findAll('div', {'class': 'f-test-vacancy-item'})
    print(f'Обработка {i+1} страницы из {max_page}')

        # Парсит блоки на текущей странице
    for vacancy in vacancy_list:
        # print('.',end='')
        vacancy_name = vacancy.find('a').getText()
        firm_name = vacancy.findAll('a')[1].getText()
        
        if vacancy_name == '':
            vacancy_name = vacancy.findAll('a')[1].getText()
            firm_name = vacancy.findAll('a')[2].getText()
            
        vacancy_link = main_link_sj + vacancy.find('a')['href']
        
        location = vacancy.find('span', {'class': 'f-test-text-company-item-location'}).findChildren()[1].getText().split(',')
        if not location:
            location = None
        city = location[0]
        metro_station = None
        if len(location) > 1:
            metro_tmp = location[1:]
            metro_station = ''
            for i in range(len(metro_tmp)):
                metro_station += metro_tmp[i] + ' '
                
                
        salary_block = vacancy.find('span', {'class': 'f-test-text-company-item-salary'}).findChildren()
        
        if len(salary_block) == 4:
            salary_min = salary_block[0].getText().replace('\xa0', '')
            salary_max = salary_block[2].getText().replace('\xa0', '')
        elif len(salary_block) == 2:
            search_condition = vacancy.find('span', {'class': 'f-test-text-company-item-salary'}).getText().replace('\xa0', ' ').split(' ')
            if search_condition[0] == 'от':
                salary_min = search_condition[1] + search_condition[2]
                salary_max = None
            elif search_condition[0] == 'до':
                salary_min = None
                salary_max = search_condition[1] + search_condition[2]
            elif search_condition[0] == 'По':
                salary_min = None
                salary_max = None
            else:
                salary_min = search_condition[0] + search_condition[1]
                salary_max = salary_min
        publish_date = vacancy.find('span', {'class': 'f-test-text-company-item-location'}).findChildren()[0].getText()
        decribe_block = vacancy.find('div', {'class': '_1tH7S _10Aay _3C76h _3achh _3ofxL _2_FIo'}).getText()
        desc = re.split('\Должностные обязанности: |Требования: ', decribe_block)
        try:
            tasks_shrt = desc[1]
        except:
            tasks_shrt = None
        try:
            prereq_shrt = desc[2]
        except:
            prereq_shrt = None
            
            
            
        
        
        
        data_sj.append({
                    'vacancy_name': vacancy_name,
                    'firm_name': firm_name,
                    'vacancy_link': vacancy_link,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'publish_date': publish_date,
                    'tasks_shrt': tasks_shrt,
                    'prereq_shrt': prereq_shrt,                    
                    'city': city,
                    'metro_station': metro_station,
                    'site': 'superjob.ru'

            })
 

    time.sleep(2 + np.random.rand())


# In[400]:


ordered_cols = ['firm_name', 'vacancy_name', 'salary_min', 'salary_max',
                'city', 'metro_station', 'prereq_shrt', 'tasks_shrt', 'publish_date', 'vacancy_link', 'site']
df_sj = pd.DataFrame.from_dict(data_sj)
df_sj = df_sj[ordered_cols]


# In[401]:


df_sj


# In[410]:


df = df_hh.append(df_sj, ignore_index=True)
df


# In[411]:


df.to_csv('job_search.csv',index=None)


# In[ ]:




