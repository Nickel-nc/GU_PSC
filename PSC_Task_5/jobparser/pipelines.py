# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from jobparser.spiders.sjru import SjruSpider
from jobparser.spiders.hhru import HhruSpider

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['PSC_5']

    def process_hh(self, item):
        item['salary_min'] = None
        item['salary_max'] = None

        # process salary
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

            #process etc... pass
        return item['salary_min'], item['salary_max']

    def process_sj(self, item):
        item['salary_min'] = None
        item['salary_max'] = None

        salary_block = item['salary'].replace('\xa0',' ')
        sal = salary_block.split()
        print(len(sal))
        if len(sal) == 2:
            item['salary_max'] = int(sal[0] + sal[1])
        # elif salary_block.find('до') != -1:
        #      item['salary_max'] = int(salary_block.split()[1] + salary_block.split()[2])
        #  elif salary_block.find('-') != -1:
        #      item['salary_min'] = int((salary_block.split('-')[0]).replace(' ', ''))
        #      item['salary_max'] = int((salary_block.split('-')[1]).split(' ')[0] + (salary_block.split('-')[1]).split(' ')[1])

            #process etc... pass
        return item['salary_min'], item['salary_max']



    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        if spider.name == SjruSpider.name:
            self.process_sj(item)
        elif spider.name == HhruSpider.name:
            self.process_hh(item)
        collection.update_one({'vacancy_link': item['vacancy_link']},
                      {'$set': item}, upsert=True)
        # collection.insert_one(item)
        return item