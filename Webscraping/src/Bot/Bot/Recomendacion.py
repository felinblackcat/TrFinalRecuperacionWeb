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
        
#****************************************************************************************************************
#********** SISTEMA DE RECOMENDACION COLABORATIVO (USUARIO - USUARIO)********************************************
#****************************************************************************************************************
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
#********************************************************************************
#************************* FIN COLABORATIVO *************************************
#********************************************************************************


#**********************************************************************************
#************************** SISTEMA HIBRIDI ***************************************
#**********************************************************************************

#Funcion para calcular y modificar lso pesos d los sistemas basado en su precision
def pesos():
  #consultar la tabla precision para computar los aciertos de las recomendaciones
  df_precision = conexion_bd("precision")
 #Verificar que el dataframe que almacena la consulta no este vacio
  if not df_precision.empty:
    colabora = df_precision[df_precision['SISTEMA_RECOMENDACION'] == "Colaborativo"]
    conten = df_precision[df_precision['SISTEMA_RECOMENDACION'] == "Contenido"]
    lcola = colabora['CALIFICACION'].tolist()
    lconte = conten['CALIFICACION'].tolist()

    c,d = 0,0
    for x in lcola:
      if x == True:
        c = c+1
    for y in lconte:
      if y == True:
        d = d+1
#calculo de los pesos, total positivos / total calificaciones, por cada RS independiente
    if len(lcola) > 0:  
      wcol = c/len(lcola)
    else:
      wcol = 1

    if len(lconte) > 0:
      wcont= d/len(lconte)
    else:
      wcont = 1
    
    resultado = [wcol, wcont]
 # en caso de estar vacio se asignan pesos de 1
  else:
    resultado = [1,1]
  return resultado

#funcion de recomendacion principal, la que se invoca para mostrar las recomendaciones
def recomendacion (usuario):
#invocar la función pesos
  pesos = pesos()
  wColaborativo = pesos[0]
  wContenido = pesos[1]

#*****obtener las recomendaciones de los sistemas de recomendacion independientes***
# Obtener la lista que arroja el sistema colaborativo, invocandolo
  topColaborativo = colaborativo(usuario)
  topColaborativo = [[x[0], x[1], "Colaborativo"] for x in topColaborativo]
  #listaColab = [[modelo, calificacion, "colaborativo"] for modelo, calificacion in topColaborativo
  
  topColaborativo = [[x[0],x[1]*wColaborativo, x[2]] for x in topColaborativo]

  topContenido = contenido()
  listaConte =[] # *****************No sé como lo saca Chaves **********************
  #  multiplicarl la calificación por el peso del RS
  listaConte = [[x[0],x[1]*wContenido, x[2]] for x in listaConte]

#Fusionarlas y ordenarlas por calificación
  listaB = topColaborativo + listaConte
  listaB2 = listaB.sort(key= lambda cal : cal[1], reverse=True)
#Eliminar modelos repetidos, conservando el de mayor calificación
  listaHibrido = []
  modelos =[]
  for i in listaB2:
    if i[0] not in modelos:
      listaHibrido.append(i)
      modelos.append(i[0])

  #*************** Insertar las recomendaciones en la tabla Precision*************
  try:
    connection = psycopg2.connect(user="postgres",
                                    password="Felingato1992",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="tvrec")
    cursor = connection.cursor()

    postgres_insert_query = """ INSERT INTO Precision ( MODELO , SISTEMA_RECOMENDACION ) VALUES (%s,%s)"""

    for valores in listaHibrido:
      insert_tuple = (valores[0], valores[2])
      cursor.execute(postgres_insert_query, insert_tuple)

      connection.commit()
      count = cursor.rowcount

  except (Exception, psycopg2.Error) as error :
      if(connection):
          print("Failed to insert record into mobile table", error)

  finally:
      #closing database connection.
      if(connection):
          cursor.close()
          connection.close()
          print("PostgreSQL connection is closed")
  #*******************************************************************
  # Regresar la lista de modelos recomendada
  return modelos

#***********************************************************************************
#************************ FIN HIBRIDI **********************************************
************************************************************************************

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
