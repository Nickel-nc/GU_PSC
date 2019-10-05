# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline

replacements = {
    'Марка': 'brand',
    'Модель': 'model',
    'Поколение': 'generation',
    'Модификация': 'modification',
    'Год выпуска': 'make_year',
    'Пробег': 'mileage_km',
    'Состояние': 'condition',
    'Владельцев по ПТС': 'PTS_owners',
    'VIN или номер кузова': 'VIN_num',
    'Тип кузова': 'body_type',
    'Количество дверей': 'num_doors',
    'Тип двигателя': 'engine_type',
    'Коробка передач': 'drive_gear',
    'Привод': 'transmission',
    'Руль': 'steering_wheel',
    'Цвет': 'color',
    'Комплектация': 'equipment',
    'Место осмотра': 'place',
    'Объем двигателя': 'engine_volume'
}


class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.PSC_6

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        data = {}
        for field in item:
            data[field] = item.get(field)

        d = item['params']
        for param in d:
            if param in replacements:
                data[replacements[param]] = d.get(param)

        del data['params']
        if data['make_year']:
            data['make_year'] = int(data['make_year'])
        if data['mileage_km']:
            data['mileage_km'] = int(data['mileage_km'].split()[0])
        collection.update_one({'link': data['link']},
                              {'$set': data}, upsert=True)
        return item

class AvitoPhotosPipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item