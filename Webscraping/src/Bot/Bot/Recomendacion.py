# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 12:14:57 2020

@author: Acer
"""
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import Reader
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import psycopg2


#---------------------------------------------------------------------------Extraccion de datos base de datos---------------------------
db_connection= psycopg2.connect(user = "postgres",password = "Felingato1992",host = "127.0.0.1",port = "5432",database = "tvrec")
cursor = db_connection.cursor()
sql_command = "SELECT * FROM {}.{};".format(str("public"), str("televisorbb"))
data = pd.read_sql(sql_command, db_connection)

#-------------------------------------------------------------------Modificar para el sistema de recomendacion----------------
reader = Reader(rating_scale=(1, 5))
#modificardeaceurdoatabla
datos = Dataset.load_from_df(data[['userId', tvid, 'rating']], reader)