# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 11:37:00 2020

@author: Acer
"""

from src.Bot.Bot.spiders.Televisoresbestbuy import TelevisoresbestbuySpider
from src.Bot.Bot.spiders.TelevisoresWalmart import TelevisoreswalmartSpider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging



configure_logging()
runner = CrawlerRunner()
@defer.inlineCallbacks
def startScan():
    
    yield runner.crawl(TelevisoresbestbuySpider)
    yield runner.crawl(TelevisoreswalmartSpider)
    reactor.stop()
    
    

startScan()
reactor.run()