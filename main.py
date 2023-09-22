import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from datetime import datetime
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/userdata/{user_id}")
def userdata(user_id: str):
    user_id = user_id.lower()
    tabla = pq.read_table('steam_games', columns=['item_id', 'price'])
    df_items = tabla.to_pandas()
    tabla = pq.read_table('users_items', columns=['user_id', 'item_id', 'items_count'])
    df_users = tabla.to_pandas()
    tabla = pq.read_table('user_reviews', columns=['user_id', 'recommend'])
    df_reviews = tabla.to_pandas()
    #Carga de datos de usuario
    usuario = df_users.loc[df_users['user_id'] == user_id]
    if usuario.empty:
        return {"Error": "Usuario inexistente"}
    usuario = usuario.merge(df_items, on='item_id', how='inner')
    #Cantidad de dinero gastado por el usuario
    gasto = usuario['price'].sum()
    gasto = round(gasto, 2)
    #Porcentaje de recomendacion de usuario
    usuario = usuario.merge(df_reviews, on= 'user_id', how= 'inner')
    conteo = usuario['recommend'].value_counts()
    true = conteo[True]
    porcentaje = (true / len(usuario['recommend'])) * 100
    porcentaje = int(porcentaje)
    #Cantidad de items consumidos por el usuario
    items = usuario.loc[0, 'items_count']
    
    return {"gasto_total_usuario": f"{gasto}", "Porcentaje_recomendacion": f"{porcentaje}", "Items_usuario": f"{items}"}


@app.get("/countreviews/{a}")
def countreviews(fecha:str):
    fecha = fecha.split('-')
    desde = fecha[0]
    hasta = fecha[1]

    numeros = re.findall(r'\d', desde)#Filtrar numeros de la fecha ingresada
    desde = ''.join(numeros)#Crear string con solamente numeros
    desde = datetime.strptime(desde, "%Y%m%d").date()#Transformar a variable datetime
    desde = desde.strftime("%Y%m%d")
    numeros = re.findall(r'\d', hasta)
    hasta = ''.join(numeros)
    hasta = datetime.strptime(hasta, "%Y%m%d").date()
    hasta = hasta.strftime("%Y%m%d")
    #importar dataset
    tabla = pq.read_table('user_reviews', columns=['posted', 'recommend', 'user_id'])
    df_reviews = tabla.to_pandas()
    #Acceder a dataset entre fechas dadas
    reviews = df_reviews.loc[(df_reviews['posted'] >= desde) & (df_reviews['posted'] <= hasta)]
    #Cantidad de usuarios
    usuarios = reviews['user_id'].nunique()

    conteo = reviews['recommend'].value_counts()
    true = conteo[True]
    porcentaje = (true / len(reviews['recommend'])) * 100
    porcentaje = int(porcentaje)

    return {"Cantidad_usuarios_reviews": f'{usuarios}', "Porcentaje_recomendacion": f'{porcentaje}'}

@app.get("/genre/{genero}")
def genre(genero: str):
    genero = genero.lower()
    tabla = pq.read_table('users_items', columns=['item_id', 'playtime_forever'])
    df_users = tabla.to_pandas()
    tabla = pq.read_table('genres', columns=['item_id', 'genres'])
    df_genres = tabla.to_pandas()
    genres = df_genres.merge(df_users, on='item_id', how='inner')
    ranking = genres.groupby('genres')['playtime_forever'].sum().reset_index()
    ranking = ranking.sort_values(by='playtime_forever', ascending=False)
    ranking = ranking[ranking['genres'] == genero].iloc[0]
    puesto = ranking.name

    return {"Puesto_ranking_playtime_forever": f'{puesto}'}

@app.get("/userforgenre/{genero}")
def userforgenre(genero: str):
    genero = genero.lower()
    tabla = pq.read_table('users_items', columns=['item_id', 'playtime_forever', 'user_id', 'user_url'])
    df_users = tabla.to_pandas()
    tabla = pq.read_table('genres', columns=['item_id', 'genres'])
    df_genres = tabla.to_pandas()
    df_genres = df_genres[df_genres["genres"].str.contains(genero, case=False)]
    df_genres = df_genres.merge(df_users, on='item_id', how='inner')
    ranking = df_genres.groupby('user_id')['playtime_forever'].sum().reset_index()
    ranking['user_url'] = df_genres['user_url']
    ranking = ranking.sort_values(by='playtime_forever', ascending=False)
    ranking = ranking[['user_id', 'user_url']].head(5).reset_index()
    lista_dicc = []
    for i in range(len(ranking)):
        diccionario = {f"{i + 1}° puesto": {"id": f"{ranking.loc[i, 'user_id']}", "url": f"{ranking.loc[i, 'user_url']}"}}
        lista_dicc.append(diccionario)
    return lista_dicc


@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):
    desarrollador = desarrollador.lower()
    tabla = pq.read_table('developer', columns=['item_id', 'developer'])
    df_developer = tabla.to_pandas()
    tabla = pq.read_table('steam_games', columns=['item_id', 'release_date', 'free'])
    df_items = tabla.to_pandas()
    df_developer = df_developer[df_developer["developer"].str.contains(desarrollador, case=False)]
    df_developer = df_developer.merge(df_items, on='item_id', how='inner')
    items = df_developer['item_id'].unique()
    items = df_developer['item_id'].value_counts()
    items = int(items.iloc[0])
    df_developer = df_developer.groupby('release_date')['free'].value_counts(normalize=True).unstack(fill_value=0).reset_index()
    df_developer['porcentaje'] = df_developer[True] / (df_developer[True] + df_developer[False]) * 100
    df_developer['porcentaje'] = df_developer['porcentaje'].astype(int)
    developer = []
    for i in range(len(df_developer)):
        dicc = {'anio': f"{df_developer.loc[i, 'release_date']}", '%_recomendacion': f"{df_developer.loc[i, 'porcentaje']}"}
        developer.append(dicc)
    
    
    return developer

@app.get("/sentiment_analysis/{anio}")
def sentiment_analysis(anio: int):
    tabla = pq.read_table('steam_games', columns=['item_id', 'release_date'])
    df_items = tabla.to_pandas()
    tabla = pq.read_table('user_reviews', columns=['item_id', 'sentiment_analysis'])
    df_reviews = tabla.to_pandas()
    df_items = df_items.merge(df_reviews, on='item_id', how='inner')
    df_items = df_items[df_items['release_date'] == anio]
    df_items = df_items.groupby('release_date')['sentiment_analysis'].value_counts().reset_index()
    positivo = df_items[df_items['sentiment_analysis'] == 2]
    positivo = positivo['count']
    neutral = df_items[df_items['sentiment_analysis'] == 1]
    neutral = neutral['count']
    negativo = df_items[df_items['sentiment_analysis'] == 0]
    negativo = negativo['count']

    return {"Negativo": f"{int(negativo)}", "Neutral": f"{int(neutral)}", "Positivo": f"{int(positivo)}"}

@app.get("/recomendacion_juego/{id_producto}")
def recomendacion_juego(id_producto):
    tabla = pq.read_table('steam_games')
    df_items = tabla.to_pandas()
    tabla = pq.read_table('genres')
    df_genres = tabla.to_pandas()

    df_items = df_items.merge(df_genres, on='item_id', how='inner')
   
    producto = df_items[df_items['item_id'] == id_producto]
    df_items = df_items[df_items['item_id'] != id_producto]
    
    primer_coincidencia_df = producto.iloc[0]
    
    
    if primer_coincidencia_df.empty:
        error = {'error': "f'{id_producto} parametro incorrecto"}
        return error 

    anio = primer_coincidencia_df['release_date']

    #Reducir el df a los items del mismo año de lanzamiento (por limitaciones de memoria ram)
    df_items = df_items[df_items['release_date'] == anio]

    #Aplicar label encoding a df_reducido
    label_encoder = LabelEncoder()
    df_encoded = df_items.apply(label_encoder.fit_transform)

    #Similitud de coseno a df_encoded
    similitud = cosine_similarity(df_encoded)

    #Debido a que el indice del dato de entrada es 0, separamos la primera fila de la matriz en un array

    array_similitud = similitud[0]

    #Obtener los indices de los 6 valores mas altos
    indices = np.argsort(-array_similitud)[:6]
    #obtener titulos
    lista_title = df_items['title']

    #Creamos una lista vacia 'respuesta', iteramos los indices y agregamos el valor de lista_title para cada indice
    respuesta = []

    for elemento in indices:
        respuesta.append(lista_title.iloc[elemento])

    respuesta = respuesta[1:]

    return {'lista recomendada': respuesta}



if __name__ == "__main__":
        uvicorn.run(app)