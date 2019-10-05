# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from AvitoParser.items import AvitoAvto
from scrapy.loader import ItemLoader

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/avtomobili']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        city = response.xpath('//div[@class="data"]/p/text()').extract()

        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads, cb_kwargs={'city': city})
        pass

    def parse_ads(self, response: HtmlResponse, city):

        loader = ItemLoader(item=AvitoAvto(), response=response)

        parameters = response.xpath('//div[@class="item-view-block"]//li/span/text()').getall()
        parameters_values = response.xpath('//div[@class="item-view-block"]//li/span/following-sibling::text()').getall()

        loader.add_xpath('photos','//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_xpath('title', '//h1[@class="title-info-title"]/span/text()')
        loader.add_xpath('price', '//div[@class="item-price-value-wrapper"]//span[@class="js-item-price"]/@content')
        loader.add_xpath('currency', '//div[@class="item-price-value-wrapper"]//span[@itemprop="priceCurrency"]/@content')
        loader.add_value('params', zip(parameters, parameters_values))
        loader.add_value('city', city)
        loader.add_value('link', response.url)


        yield loader.load_item()
