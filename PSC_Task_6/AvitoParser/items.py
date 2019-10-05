# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst



def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def cleaner_price(values):
    try:
        return int(values)
    except:
        return None
def cleaner_city(values):
    try:
        return values.split(',')[1]
    except:
        return None

def process_params(params):
    return dict((x.replace(x[-1], ''), y.replace(y[-1],'')) for x, y in params)


class AvitoAvto(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(input_processor=MapCompose(cleaner_price), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(input_processor=process_params, output_processor=TakeFirst())
    city = scrapy.Field(output_processor=TakeFirst())
