# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 11:37:00 2020

@author: Acer
"""

from spiders.Televisoresbestbuy import TelevisoresbestbuySpider
from spiders.TelevisoresWalmart import TelevisoreswalmartSpider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import psycopg2




settings = get_project_settings()  
configure_logging(settings)
runner = CrawlerRunner(settings)





@defer.inlineCallbacks
def startScan():
    yield runner.crawl(TelevisoreswalmartSpider)
    yield runner.crawl(TelevisoresbestbuySpider)    
    
    reactor.stop()
  

    


startScan()
reactor.run()


