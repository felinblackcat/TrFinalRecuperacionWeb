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
#Propios
import io
import pandas as pd
from surprise import Reader
from surprise import Dataset
from surprise import KNNWithMeans
from surprise.model_selection import GridSearchCV
from surprise import SVD
from collections import defaultdict

#Funciones
def get_top_n(predictions, n=5):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def conexion_bd(tabla):
    #---------------------------------------------------------------------------Extraccion de datos base de datos---------------------------
    #Conexión a la Base de datos
    try:
        db_connection= psycopg2.connect(user = "postgres",password = "Felingato1992",host = "127.0.0.1",port = "5432",database = "tvrec")
        
        # Extracción de datos de la Base de datos
        sql_command = "SELECT * FROM {}.{};".format(str("public"), str(tabla))
        df_tabla = pd.read_sql(sql_command, db_connection)
    
    except (Exception, psycopg2.Error) as error :
            print("Failed PostgreSQL connection", error)

    finally:
        db_connection.close()
        print("PostgreSQL connection is closed")
            
    return df_tabla
        

def colaborativo(usuario):

    df_calificacion = conexion_bd("calificacion")
    
    
    #if usuario in df_calificacion.values:
        
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df_calificacion, reader)
        
    SVD_Op = SVD(n_epochs=5,lr_all=0.002,reg_all=0.8)
    trainingSet = data.build_full_trainset()
    SVD_Op.fit(trainingSet)
        
    testset = trainingSet.build_anti_testset()
    predictions = SVD_Op.test(testset)
        
    top_n = get_top_n(predictions, n=10)
    topuser = [modelo, calificacion for modelo, calificacion in top_n[usuario]]
        
    return topuser
    

"""
if __name__ == "__main__":
    
    usuario = "U1@gmail.com"
    top_n = recomendacion(usuario)
    
    print("Televisores y calificaciones predichas:")
    print(" ")
    
    for item, rating in top_n[usuario]:
        print("Televisor recomendado para {} {} con calificación de {}".format(usuario,item,rating))
    
    print(top_n.values())  
"""


#df_usuario = conexion_bd("usuario")
#df_televisor = conexion_bd("televisor") 
