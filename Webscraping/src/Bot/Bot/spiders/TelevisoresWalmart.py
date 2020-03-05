# -*- coding: utf-8 -*-
import scrapy


class TelevisoreswalmartSpider(scrapy.Spider):
    name = 'TelevisoresWalmart'
    allowed_domains = ['https://www.walmart.com/browse/tv-video/all-tvs/3944_1060825_447913']
    start_urls = ['http://https://www.walmart.com/browse/tv-video/all-tvs/3944_1060825_447913/']

    def parse(self, response):
        pass
