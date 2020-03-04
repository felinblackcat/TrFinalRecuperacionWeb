# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 12:26:14 2020

@author: Acer
"""

class televisor:
    
    def __init__(self,Modelo,Caracteristicas,Marca,Precio,TamañoPantalla,Resolucion,TipoDisplay,url):
        
        self.Modelo = Modelo
        self.Caracteristicas = Caracteristicas
        self.Marca = Marca
        self.Precio = Precio
        self.TamañoPantalla = TamañoPantalla
        self.Resolucion = Resolucion
        self.TipoDisplay = TipoDisplay
        self.url = url
        
    def getModelo(self):
        return(self.Modelo)
        
    def getCaracteristicas(self):
        return(self.Caracteristicas)
        
    def getMarca(self):
        return(self.Marca)
        
    def getPrecio(self):
        return(self.Precio)
        
    def getTamañoPantalla(self):
        return(self.TamañoPantalla)
        
    def getResolucion(self):
        return(self.Resolucion)
        
    def getTipoDisplay(self):
        return(self.TipoDisplay)
        
    def geturl(self):
        return(self.url)
        
    def setModelo(self,Modelo):        
        self.Modelo = Modelo
        
    def setCaracteristicas(self,Caracteristicas):
        self.Caracteristicas = Caracteristicas
        
    def setMarca(self,Marca):
        self.Marca = Marca
        
    def setPrecio(self,Precio):
        self.Precio = Precio
        
    def setTamañoPantalla(self,TamañoPantalla):
        self.TamañoPantalla = TamañoPantalla
        
    def setResolucion(self,Resolucion):
        self.Resolucion = Resolucion
        
    def setTipoDisplay(self,TipoDisplay):
        self.TipoDisplay = TipoDisplay
        
    def setUrl(self,url):
        self.url = url