# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    vacancy_name = scrapy.Field()
    salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    firm_name = scrapy.Field()
    vacancy_link = scrapy.Field()
    publish_date = scrapy.Field()
    address_raw = scrapy.Field()
    site = scrapy.Field()
