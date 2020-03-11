# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

class BotPipeline(object):
    
        
    
    def open_spider(self, spider):
        self.db_connection= psycopg2.connect(user = "postgres",password = "Felingato1992",host = "127.0.0.1",port = "5432",database = "tvrec")
        self.cursor = self.db_connection.cursor()
    
    def close_spider(self, spider):
        self.db_connection.close()
    
    def process_item(self, item, spider):   
       # insercion = "INSERT INTO televisores(Modelo,Marca,Precio,TamañoPantalla,Resolucion,TipoDisplay,url)"
       
       if(item["url"].find('https://www.bestbuy.com')>=0): 
       
            sql = "INSERT INTO TELEVISORBB(modelo,marca,Precio,tamaÑopantalla,resoluciÓn,tipodisplay,urlbb,calificaciÓnbb,activo) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (item['Modelo'],item['Marca'],item['Precio'],item['TamañoPantalla'],item['Resolucion'],item['TipoDisplay'],item["url"],item['Calificacion'],item["activo"])
            self.cursor.execute(sql,values)
            self.db_connection.commit()
       else:
           sql = "INSERT INTO televisorwalmart(modelo,marca,Precio,tamaÑopantalla,resoluciÓn,tipodisplay,urlwalmart,calificaciÓnwalmart,activo) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
           values = (item['Modelo'],item['Marca'],item['Precio'],item['TamañoPantalla'],item['Resolucion'],item['TipoDisplay'],item["url"],item['Calificacion'],item["activo"])
           self.cursor.execute(sql,values)
           self.db_connection.commit()
        
       return item
    
    
        
        
        
    