# -*- coding: utf-8 -*-
import scrapy
import sys
from scrapy.spiders import CrawlSpider,Rule
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from src.Bot.Bot.items import BotItem
import cfscrape
from Bot.WebScraping import WebScraping
from bs4 import BeautifulSoup

class TelevisoreswalmartSpider(scrapy.Spider):
    name = 'TelevisoresWalmart'
    page_count = 1    
    dominio = 'https://www.walmart.com'
    SCRAP = WebScraping()    
    ListaHost = SCRAP.scrapingLinkHost1()    
    
    
    
    def start_requests(self):        
        urls = self.ListaHost # url inicial (lista televisores)
        token,agent = cfscrape.get_tokens(url="https://www.walmart.com/browse/tv-video/all-tvs/3944_1060825_447913/?page=1")
        self.token = token
        self.agent = agent
        self.max = 10000
        self.pages = 1000
        for url in urls:
            #Bypass para cloudflare
            
            yield scrapy.Request(url=url,callback=self.parse,cookies=token,headers={'User-Agent': agent})
        #yield scrapy.Request(url=urls[1],callback=self.parse,cookies=token,headers={'User-Agent': agent})    
    
    
    
    def parse(self, response):
        
        TelevisoresPagina = response.xpath('//div[@class="search-product-result"]//ul[@class="search-result-gridview-items four-items"]//li')
        Televisores = TelevisoresPagina.xpath('//div[@class="search-result-product-title gridview"]//a/@href').extract()
        
        for televisor in Televisores:
            #print(self.dominio+televisor)  
            respuesta = response.follow(self.dominio+televisor,callback=self.TelevisionData,cookies=self.token,headers={'User-Agent': self.agent})
            respuesta.meta['URL'] = self.dominio+televisor
            
            yield respuesta
        
        pass

    def TelevisionData(self,res):     
        Televisor = BotItem()
        try:
            caracteristicas = BeautifulSoup(res.text, 'html5lib').find('div',class_='SpecHighlights-container').find('ul',class_='SpecHighlights-list Grid text-left').find_all('li',class_='Grid-col u-size-12-12-xs u-size-6-12-s u-size-4-12-m text-center')
            
            for caracteristica in caracteristicas:
                dato = caracteristica.find('div',class_='SpecHighlights-list-item')
                label = dato.find('div',class_='SpecHighlights-list-label').text.strip()
                valor = dato.find('div',class_='SpecHighlights-list-value').text.strip()
                if(label=="Screen Size"):
                    Televisor["TamañoPantalla"]=valor.split('"')[0]
                    
                elif(label=="Resolution"):
                    Televisor["Resolucion"]=valor
                    
                elif(label=="Display Technology"):
                    Televisor["TipoDisplay"]=valor  
                    
            datos2 = BeautifulSoup(res.text, 'html5lib').find('div',class_='hf-Bot').find('div',class_='prod-productsecondaryinformation display-inline-block prod-SecondaryInfo')
            Televisor["Modelo"] = datos2.find('div',class_='valign-middle secondary-info-margin-right copy-mini display-inline-block other-info').text.strip().split("Model: ")[1]
            Televisor["Marca"] = datos2.find('div',class_='valign-middle secondary-info-margin-right copy-mini display-inline-block').a.span.text.strip()
            Televisor["Precio"] = float(BeautifulSoup(res.text, 'html5lib').find('div',class_='prod-PriceHero').find('span',class_='hide-content display-inline-block-m').find('span',class_='price display-inline-block arrange-fit price price--stylized').find('span',class_='visuallyhidden').text.strip().split('$')[1])
            calificacion = BeautifulSoup(res.text, 'html5lib').find('div',class_='CustomerReviews-container').find('div',class_='ReviewsHeader-ratingContainer').span.span.text.strip()   
            Televisor["Calificacion"]=float(calificacion)
            Televisor["url"] = res.meta.get('URL')
            
            
        except:
            #No es televisor XD
            print("No es televisor.")
        
        return Televisor    
        
            
              
        

