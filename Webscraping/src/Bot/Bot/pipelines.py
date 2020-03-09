# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class BotPipeline(object):
    
        
    
    def open_spider(self, spider):
        self.db_connection=MySQLdb.connect("localhost","root","","WebScraping")
        self.cursor = self.db_connection.cursor()
    
    def close_spider(self, spider):
        self.db_connection.close()
    
    def process_item(self, item, spider):   
       # insercion = "INSERT INTO televisores(Modelo,Marca,Precio,TamañoPantalla,Resolucion,TipoDisplay,url)"
        sql = "INSERT INTO televisores(Modelo,Marca,Precio,TamañoPantalla,Resolucion,TipoDisplay,url) values(%s,%s,%s,%s,%s,%s,%s)"
        values = (item['Modelo'],item['Marca'],item['Precio'],item['TamañoPantalla'],item['Resolucion'],item['TipoDisplay'],"pagina.com")
        self.cursor.execute(sql,values)
        self.db_connection.commit()
        
        return item
    
    
        
        
        
    