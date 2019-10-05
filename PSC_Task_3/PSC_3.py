# ## Методы сбора и обработки данных из сети Интернет

# ### Парсинг HTML. Mongo DB

# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД
# 2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
# 3*)Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта


from pymongo import MongoClient
import pandas as pd
import json
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['PSC_3']
jobs_hh = db.jobs_hh
jobs_sj = db.jobs_sj

df_hh = pd.read_csv('job_search_hh.csv')
df_sj = pd.read_csv('job_search_sj.csv')

df_hh.head()

df_sj.head()

# Clear all data in db
def clear_db(db):
    db.delete_many({})
    
# Add all data to db
def df_to_db(df, db_collection):
    data = json.loads(df.T.to_json()).values()
    db_collection.insert_many(data)

# Update Mongo database with upsert
def update_db(df, db):
    data = json.loads(df.T.to_json()).values()
    for item in data:
        db.update_one({'vacancy_link':item['vacancy_link']},
                      {'$set':item}, upsert = True)

# Searching for salary
def show_search_results(db, amount=200000, func='gt', params):
    n = db.find({'salary_max':{f'${func}':amount}}, params)
    for item in n:
        pprint(item)


# clear_db(jobs_hh)
# clear_db(jobs_sj)

# df_to_db(df_hh, jobs_hh)
# df_to_db(df_sj, jobs_sj)

# pprint(show_search_results(jobs_hh, amount, func, params))
# pprint(show_search_results(jobs_sj, amount, func, params))

update_db(df_hh, jobs_hh)
update_db(df_sj, jobs_sj)


params = {'firm_name', 'vacancy_name', 'salary_min', 'salary_max', 'city',
       'metro_station', 'prereq_shrt', 'tasks_shrt', 'publish_date',
       'vacancy_link', 'site'}

pprint(show_search_results(jobs_hh, amount, func, params))
pprint(show_search_results(jobs_sj, amount, func, params))



