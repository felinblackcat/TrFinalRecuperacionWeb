# -*- coding: utf-8 -*-
import scrapy

from src.Bot.Bot.WebScraping import WebScraping
from src.Bot.Bot.items import BotItem
import cfscrape
from bs4 import BeautifulSoup
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


class TelevisoreswalmartSpider(scrapy.Spider):
    
        
    name = 'TelevisoresWalmart'
    page_count = 1    
    dominio = 'https://www.walmart.com'
    SCRAP = WebScraping()    
    ListaHost = SCRAP.scrapingLinkHost1()    
    ValidadorTelevisor={'Screen Size':'','Resolution':'','Is Smart':'','Display Technology':'','Backlight Type':''}
    
        
        
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
        html = BeautifulSoup(response.text, 'html5lib')
        
        TelevisoresPagina = html.find('div',class_='search-product-result').find('ul',class_='search-result-gridview-items four-items')
        Televisores = TelevisoresPagina.find_all('li')
        for Televisor in Televisores:
            link = self.dominio+Televisor.find('div',class_='search-result-product-title gridview').find('a')['href']
            respuesta = response.follow(link,callback=self.TelevisionData,cookies=self.token,headers={'User-Agent': self.agent})
            respuesta.meta['URL'] = link            
            yield respuesta
        pass

    def TelevisionData(self,res):  
        html = BeautifulSoup(res.text, 'html5lib')
        Televisor = BotItem()
        Televisor['url'] = res.meta.get('URL')
        bandera = True
        try:
            Stock = html.find('div','text-left AboutProductSection AboutThisItem m-padding-ends').find('div',class_='Specification-container').find('table','table table-striped-odd specification')          
            
            Caracteristicas = Stock.find_all('tr') 
            for Caracteristica in Caracteristicas:
                dato = Caracteristica.find_all('td')
                tipo = dato[0].text.strip()               
                value = dato[1].text.strip()  
                
                # print(tipo)
                
                if(tipo=="Screen Size"):
                    
                    if(not(tipo in self.ValidadorTelevisor)):
                        
                        bandera = False
                        break;
                    else:   
                        Televisor['TamañoPantalla']=value.split('"')[0].split('\\')[0]
                        
                        
                elif(tipo=='Resolution'):
                    
                    if(not(tipo  in self.ValidadorTelevisor)):
                        
                        bandera = False
                        break;
                    else:
                        Televisor['Resolucion']=value
                elif(tipo=='Is Smart'):
                    
                    if(not(tipo in self.ValidadorTelevisor)):
                        
                        bandera = False
                        break;
                        
                elif(tipo=="Display Technology"):
                    
                    if(not(tipo in self.ValidadorTelevisor)):
                        
                        bandera = False
                        break;
                    else:
                        Televisor['TipoDisplay']=value
                    
                elif(tipo=="Backlight Type"):
                    
                    if(not(tipo in self.ValidadorTelevisor)):
                        
                        bandera = False
                        break;
                elif(tipo=="Model"):
                    Televisor['Modelo'] =value
                    
                elif(tipo=="Brand"):
                    Televisor['Marca'] =value
                
           
            if(bandera):
                try:
                    precio = html.find('span',class_='price display-inline-block arrange-fit price price--stylized').find('span',class_='price-characteristic')['content']
                    Televisor['Precio'] = float(precio)                    
                except:
                    Televisor['Precio']= 0
                    
                    
                try:
                    puntaje = html.find('span',class_='ReviewsHeader-ratingPrefix font-bold').text.strip()                    
                    Televisor['Calificacion']=float(puntaje)
                except:
                    Televisor['Calificacion']=0
                Televisor['activo'] = "true"
                
                if(not('TamañoPantalla' in Televisor)):  
                    Televisor['TamañoPantalla'] =' ' 
                if(not('TipoDisplay' in Televisor)):
                    Televisor['TipoDisplay']  =' '
                    
                if(not('Marca'in Televisor)):
                    Televisor['Marca']  =' '
                if(not('Resolucion'in Televisor)):                 
                    Televisor['Resolucion']=' '
                    
                if(not('Modelo'in Televisor)):
                    try:
                        Televisor['Modelo']=html.find('div',class_='valign-middle secondary-info-margin-right copy-mini display-inline-block other-info').text.strip()
                    except:
                        Televisor['Modelo']=' '
            else:
                print('No es televisor',Televisor['url'])
            
        except:
           print("fuera de stock: ",Televisor['url']) 
        
        
        yield Televisor    
  
'''
settings = get_project_settings()
#crawler = Crawler()
runner = CrawlerRunner(settings)

d = runner.crawl(TelevisoreswalmartSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished

'''




