# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 12:13:32 2020
"""
import requests
import html5lib
import scrapy
from bs4 import BeautifulSoup



class WebScraping:
    
    def __init__(self):
        self.HOST1 = "https://www.walmart.com"
        self.HOST2 = "https://www.bestbuy.com"
        self.HOST1Busqueda = "https://www.walmart.com/browse/tv-video/all-tvs/3944_1060825_447913"
        self.HOST2Busqueda = "https://www.bestbuy.com/site/tvs/all-flat-screen-tvs/abcat0101001.c?id=abcat0101001&intl=nosplash"
        self.Televisores = {}
        self.user_agent = {'User-agent': 'Mozilla/5.0'}
        #direccon de demas resultados : https://www.walmart.com/browse/tv-video/all-tvs/3944_1060825_447913/?page=2
    
    def scrapingLinkHost1(self):
        ListaCrawling = []
        page = requests.get(self.HOST1Busqueda)
        parser = BeautifulSoup(page.content, 'html5lib')
        paginador = parser.find('div',class_='paginator outline').find('ul',class_='paginator-list').find_all('li')
        NumPaginas = paginador[len(paginador)-1].a.text
        
        for Pagina in range(int(NumPaginas)+1):
            ListaCrawling.append('https://www.walmart.com/browse/tv-video/all-tvs/3944_1060825_447913/?page='+str(Pagina))
        
        return(ListaCrawling)   
        
    def scrapingLinkHost2(self):
        ListaCrawling = []        
        page = requests.get(self.HOST2Busqueda,headers=self.user_agent)
        parser = BeautifulSoup(page.content, 'html5lib') 
        paginador = parser.find('ol',class_='paging-list').find_all('li')
        NumPaginas = paginador[len(paginador)-1].a.text
        for Pagina in range(1,int(NumPaginas)+1):
            ListaCrawling.append("https://www.bestbuy.com/site/tvs/all-flat-screen-tvs/abcat0101001.c?cp="+str(Pagina)+"&id=abcat0101001&intl=nosplash")
        
        return(ListaCrawling)  
        
        
        
    

