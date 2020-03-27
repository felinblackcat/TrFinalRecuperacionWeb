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
from scrapy.utils.project import get_project_settings


configure_logging()



settings = get_project_settings()
runner = CrawlerRunner(settings)
@defer.inlineCallbacks
def startScan():
    yield runner.crawl(TelevisoreswalmartSpider)
    yield runner.crawl(TelevisoresbestbuySpider)    
    reactor.stop()
  
def proceso(value):
    print(value)
    

#startScan()
#reactor.run()



'''

d = runner.crawl(TelevisoreswalmartSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished

'''