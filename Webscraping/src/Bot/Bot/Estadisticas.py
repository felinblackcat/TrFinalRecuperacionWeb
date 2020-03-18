# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 12:36:53 2020

@author: Acer
"""

import numpy as np
import pandas as pd
import pandas.io.sql as psql
import psycopg2

db_connection= psycopg2.connect(user = "postgres",password = "Felingato1992",host = "127.0.0.1",port = "5432",database = "tvrec")
cursor = db_connection.cursor()

sql_command = "SELECT * FROM {}.{};".format(str("public"), str("televisorbb"))
data = pd.read_sql(sql_command, db_connection)
print(data.head())
print(data.count())
data.describe()
data[data.precio == 0]
data[data.calificaciÓnbb == 0]['modelo']
data["marca"].value_counts()
data["resoluciÓn"].value_counts()
data["tamaÑopantalla"].value_counts()
data["tipodisplay"].value_counts()
data["activo"].value_counts()
#cpnsulta de todas las tablas de una base de datos 
'''
SELECT table_name --seleccionamos solo la columna del nombre de la tabla
FROM information_schema.tables --seleccionamos la información del esquema 
WHERE table_schema='public' --las tablas se encuentran en el esquema publico
AND table_type='BASE TABLE'; 
'''
