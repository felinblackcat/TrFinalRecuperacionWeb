# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
from src.Bot.Bot.Señal import Foo
class BotPipeline(object):
    signal = Foo()
    
    cantidad = 0    
    
    def open_spider(self, spider):
        self.db_connection= psycopg2.connect(user = "postgres",password = "Felingato1992",host = "127.0.0.1",port = "5432",database = "tvrec")
        self.cursor = self.db_connection.cursor()
    
    def close_spider(self, spider):
        self.cursor.close()
        self.db_connection.close()
    
    def process_item(self, item, spider):  
       self.signal.connect_and_emit_trigger(str(1))
       # insercion = "INSERT INTO televisores(Modelo,Marca,Precio,TamanoPantalla,Resolucion,TipoDisplay,url)"
       
       if(item["url"].find('https://www.bestbuy.com')>=0): 
            try:
                self.cantidad = self.cantidad + 1
                print(self.cantidad)
                sql = "INSERT INTO TELEVISORBB(modelo,marca,Precio,tamanopantalla,resolucion,tipodisplay,urlbb,calificacionbb,activo) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (item['Modelo'],item['Marca'],item['Precio'],item['TamañoPantalla'],item['Resolucion'],item['TipoDisplay'],item["url"],item['Calificacion'],item["activo"])
                self.cursor.execute(sql,values)
                self.db_connection.commit()
            except Exception as error:
                self.db_connection.rollback()
                print ("Oops! An exception has occured:", error)
                print ("Exception TYPE:", type(error))
                
            
       elif(item["url"].find('https://www.walmart.com')>=0):
           if(item['Modelo']!=' '):
               
               try:
                   self.cantidad = self.cantidad + 1
                   print(self.cantidad)
                   sql = "INSERT INTO televisorwalmart(modelo,marca,Precio,tamanopantalla,resolucion,tipodisplay,urlwalmart,calificacionwalmart,activo) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                   values = (item['Modelo'],item['Marca'],item['Precio'],item['TamañoPantalla'],item['Resolucion'],item['TipoDisplay'],item["url"],item['Calificacion'],item["activo"])
                   self.cursor.execute(sql,values)
                   self.db_connection.commit()
        
               except Exception as error:
                    self.db_connection.rollback()
                    print ("Oops! An exception has occured:", error)
                    print ("Exception TYPE:", type(error))
               
               
       return item
    
    
        
        
        
    