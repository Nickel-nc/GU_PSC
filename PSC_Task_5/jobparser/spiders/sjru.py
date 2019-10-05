# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'superjob.ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response:HtmlResponse):
        # Next page button
        next_page = response.xpath(
            '//a[@rel="next"]/@href'
        ).extract_first()

        yield response.follow(next_page, callback=self.parse)

        # link for any vacancy

        # vacancy = response.xpath('//a[@target="_blank"]/@href')

        vacancy = response.xpath(
            '//div[@class="_2g1F-"]/a/@href'
        ).extract()

        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath(
            '//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]/text()'
        ).extract_first()

        salary = response.xpath(
            '//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]//text()'
        ).extract()

        salary_min = None
        salary_max = None

        firm_name = response.xpath(
            '//a[@target="_self"]/h2/text()'
        ).extract_first()

        vacancy_link = response.url

        publish_date = response.xpath(
            '//div[@class="_2g1F-"]/span[@class="_3mfro _9fXTd _2JVkc _3e53o"]//text()'
        ).extract()

        address_raw = response.xpath(
            '//span[@class="_3mfro _1hP6a _2JVkc"]/text()'
        ).extract_first()

        site = self.name

        yield JobparserItem(
            vacancy_name=vacancy_name,
            firm_name=firm_name,
            salary_min=salary_min,
            salary_max=salary_max,
            salary=salary,
            vacancy_link=vacancy_link,
            publish_date=publish_date,
            address_raw=address_raw,
            site=site
        )

