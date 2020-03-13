# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 11:37:00 2020

@author: Acer
"""

from src.Bot.Bot.spiders.Televisoresbestbuy import TelevisoresbestbuySpider
from src.Bot.Bot.spiders.TelevisoresWalmart import TelevisoreswalmartSpider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer

process = CrawlerRunner()
@defer.inlineCallbacks
def startScan():
    
    yield process.crawl(TelevisoresbestbuySpider)
    yield process.crawl(TelevisoreswalmartSpider)
    reactor.stop()
    
    

startScan()
reactor.run()