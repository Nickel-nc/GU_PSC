# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from jobparser.spiders.sjru import SjruSpider
from jobparser.spiders.hhru import HhruSpider
from datetime import datetime, timedelta
from DateDict import ru_month_dict

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['PSC_5']

    def process_hh(self, item):

        # name
        # Unite string child nodes
        item['vacancy_name'] = ' '.join(item['vacancy_name']).replace('  ', ' ')


        # Salary
        item['salary_min'] = None
        item['salary_max'] = None
        salary_block = item['salary'].replace('\xa0',' ')
        if salary_block.find('от') !=-1 and salary_block.find('до') !=-1:
            item['salary_min'] = int(salary_block.split()[1] + salary_block.split()[2])
            item['salary_max'] = int(salary_block.split()[4] + salary_block.split()[5])
        elif salary_block.find('от') != -1:
            item['salary_min'] = int(salary_block.split()[1] + salary_block.split()[2])
        elif salary_block.find('до') != -1:
            item['salary_max'] = int(salary_block.split()[1] + salary_block.split()[2])
        elif salary_block.find('-') != -1:
            item['salary_min'] = int((salary_block.split('-')[0]).replace(' ', ''))
            item['salary_max'] = int((salary_block.split('-')[1]).split(' ')[0] + (salary_block.split('-')[1]).split(' ')[1])


        # Pull publish date pre#1
        c = item['publish_date'].split()
        c[3] = ru_month_dict(c[3])
        item['publish_date'] = c[2] + ' ' + c[3] + ' ' + c[4]





        return item['salary_min'], item['salary_max'], item['vacancy_name'], item['publish_date']

    def process_sj(self, item):

        if not item['firm_name']:
            pass

        # Salary
        item['salary_min'] = None
        item['salary_max'] = None

        salary_block = item['salary']
        if len(item['salary']) > 1:
            salary_block = ' '.join(salary_block).replace('  ', ' ').replace('\xa0', ' ')
        else:
             salary_block = salary_block[0]

        sal = salary_block.split()

        if len(sal) == 3:
            item['salary_max'] = int(sal[0] + sal[1])
        elif salary_block.find('По') != -1:
            pass

        elif len(sal) == 6:
            item['salary_min'] = int(sal[0] + sal[1])
            item['salary_max'] = int(sal[3] + sal[4])

        elif salary_block.find('от') != -1:
            item['salary_min'] = int(sal[1] + sal[2])

        elif salary_block.find('до') != -1:
            item['salary_max'] = int(sal[1] + sal[2])


        #pulish date
        date = item['publish_date'][2]
        if date.find(':') != -1:
            item['publish_date'] = datetime.now().strftime("%d %m %Y")
        elif date.find('вчера') != -1:
            item['publish_date'] = (datetime.now() - timedelta(days=1)).strftime("%d %m %Y")
        else:
            c = date.split()
            c[1] = ru_month_dict(c[1])
            item['publish_date'] = c[0] + ' ' + c[1] + ' ' + c[2]




        return item['salary_min'], item['salary_max'], item['publish_date']



    def process_item(self, item, spider):

        collection = self.mongo_base[spider.name]
        if spider.name == SjruSpider.name:
             self.process_sj(item)
        if spider.name == HhruSpider.name:
            self.process_hh(item)

        # crop aid strings
        del item['salary']
        collection.update_one({'vacancy_link': item['vacancy_link']},
                      {'$set': item}, upsert=True)
        return item