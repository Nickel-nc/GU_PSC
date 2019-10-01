# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&text=Python']

    def parse(self, response:HtmlResponse):

        # Next page button
        next_page = response.xpath(
            '//a[contains(@class, "HH-Pager-Controls-Next")]/@href'
        ).extract_first()

        yield response.follow(next_page, callback=self.parse)

        # link for any vacancy
        vacancy = response.xpath(
            '//a[@class="bloko-link HH-LinkModifier"]/@href'
        ).extract()

        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response:HtmlResponse):

        vacancy_name = response.xpath(
            '//div[@class="vacancy-title "]/h1[@class="header"]/text()'
        ).extract_first()

        salary = response.xpath(
            '//p[@class="vacancy-salary"]/text()'
        ).extract_first()

        salary_min = None
        salary_max = None

        firm_name = response.xpath(
            '//a[@class="vacancy-company-name"]/span/text()'
        ).extract_first()

        vacancy_link = response.url

        publish_date = response.xpath(
            '//p[@class="vacancy-creation-time"]/text()'
        ).extract_first()

        address_raw = response.xpath(
            '//span[@data-qa="vacancy-view-raw-address"]/text()'
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




