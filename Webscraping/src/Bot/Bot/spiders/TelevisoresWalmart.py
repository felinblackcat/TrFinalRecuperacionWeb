# -*- coding: utf-8 -*-
import scrapy

from WebScraping import WebScraping
from items import BotItem
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
        try:
            caracteristicas = html.find('div',class_="product-specifications").find('table').find('tbody').find_all('tr')
            #Es televisor si tiene los atributos en la pagina de:
            #Display Technology,Resolution,Model,Screen Size,Brand,Refresh Rate, si no encuentra alguno 
            #return no este televisor       
           
            
            if(len(caracteristicas)>0):            
                for caracteristica in caracteristicas:
                    try:
                        datos = caracteristica.find_all('td')
                        name = datos[0].text.strip()
                        value = datos[1].text.strip()
                        
                        if(name =="Display Technology"):
                            Televisor['TipoDisplay'] = value
                            
                        elif(name =="Resolution"):
                            Televisor['Resolucion'] = value
                            
                        elif(name =="Model"):
                            Televisor['Modelo'] = value
                            
                        elif(name =="Screen Size"):
                            Televisor['TamañoPantalla'] = value                    
                            
                        elif(name =="Brand"):
                            Televisor['Marca'] = value
                    except Exception:
                        er = 0
                    
                #AttributeError:
                try:
                    Precio = html.find('section',class_='prod-PriceSection').find('div',class_='prod-PriceHero').find('span',class_='price display-inline-block arrange-fit price price--stylized').find('span',class_='visuallyhidden').text.strip()
                    Televisor['Precio'] = float(Precio.strip('$'))
                except Exception:
                    Televisor['Precio'] = 0
                    #Calificacion = scrapy.Field()    
                    #activo = scrapy.Field()
                try:
                    Calificacion = html.find('span',class_='ReviewsHeader-ratingPrefix font-bold').text.strip()
                    Televisor['Calificacion'] = float(Calificacion)
                except Exception:
                    Televisor['Calificacion']  = 0
                Televisor['activo'] = "true"
                try:            
                    print(Televisor['Modelo'])
                except:
                    Televisor['Modelo'] = ' '
                    print("Televisor sin Modelo")
                    
                try:
                    type(Televisor['TipoDisplay'])
                except Exception:
                    Televisor['TipoDisplay'] = ' '
                
                try:
                    type(Televisor['Resolucion'])
                except Exception:
                    Televisor['Resolucion'] = ' '
                    
                try:
                    type(Televisor['TamañoPantalla'])
                    
                except Exception:
                    Televisor['TamañoPantalla'] = ' '
                    
                try:
                    type(Televisor['Marca'])
                except Exception:
                    Televisor['Marca'] = ' '
                
                print(Televisor)
            
                
                
            else:
                print("No es televisor.")
        except AttributeError:
            #Televisor['Modelo'] = ' '
            print("Error inesperado")
            
        yield Televisor    
  





