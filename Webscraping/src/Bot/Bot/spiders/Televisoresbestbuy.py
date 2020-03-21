# -*- coding: utf-8 -*-
import scrapy
from src.Bot.Bot.WebScraping import WebScraping
from bs4 import BeautifulSoup
from src.Bot.Bot.items import BotItem
from scrapy.crawler import CrawlerProcess



class TelevisoresbestbuySpider(scrapy.Spider):
    
        
    name = 'Televisoresbestbuy'
    dominio = 'https://www.bestbuy.com'
    SCRAP = WebScraping()       
    ListaHost = SCRAP.scrapingLinkHost2()
    
    
    #donde empezara a hacer el scraping
    #start_urls = ['https://www.bestbuy.com/site/tvs/all-flat-screen-tvs/abcat0101001.c?id=abcat0101001&intl=nosplash']

    def start_requests(self): 
        
        urls = self.ListaHost
        #
        for link in urls:
           # print(link)
           yield scrapy.Request(url=link,callback=self.parse)    

    def parse(self, response):
        TelevisoresPagina = BeautifulSoup(response.text, 'html5lib').find('ol',class_='sku-item-list').find_all('li',class_='sku-item')
        for Televisor in TelevisoresPagina:
            url = self.dominio+Televisor.find('div',class_='sku-title').find('h4',class_="sku-header").find('a')['href']
            respuesta = response.follow(url,callback=self.TelevisionData)
            respuesta.meta['URL'] = url            
            yield respuesta
        pass
    def TelevisionData(self,res):     
        Televisor = BotItem()
        Televisor["url"] = res.meta.get('URL')
        html = BeautifulSoup(res.text, 'html5lib')
        page = BeautifulSoup(res.text, 'html5lib').find('div',class_='shop-specifications').find('div',class_='spec-categories').find_all('div',class_='category-wrapper row')
        spec = page[0].find('div',class_='specs-table col-xs-9').find('ul').find_all('li')
        general = page[1].find('div',class_='specs-table col-xs-9').find('ul').find_all('li')
        Televisor["TipoDisplay"]=spec[0].find('div',class_='row-value col-xs-8 v-fw-regular').text.strip()
        Televisor["Modelo"]=general[2].find('div',class_='row-value col-xs-8 v-fw-regular').text.strip()
        Televisor["Marca"]=general[1].find('div',class_='row-value col-xs-8 v-fw-regular').text.strip()
        try:
            Televisor["Precio"] = float(html.find('div',class_='priceView-hero-price priceView-customer-price').span.text.split('$')[1].replace(',',''))
        except:
            Televisor["Precio"]=0
        Televisor["TamañoPantalla"]=spec[2].find('div',class_='row-value col-xs-8 v-fw-regular').text.strip()
        Televisor["Resolucion"]=spec[1].find('div',class_='row-value col-xs-8 v-fw-regular').text.strip()  
        try:
            Televisor["Calificacion"]=float(html.find('div',class_='user-generated-content-ugc-stats').find('div','appContainer size-l').find('ul',class_='reviews-stats-list').find_all('li')[0].find('span',class_='c-review-average').text)
        except:
            Televisor["Calificacion"]=float(0)
        Televisor["activo"]="true"
        
        return(Televisor)    
    
 
    
    
    
    
    
    
    
    
    
