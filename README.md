Descripción del código
A partir del uso de la biblioteca pandas en Python, este código desarrolla una serie de transformaciones y análisis de datos. El código se encuentra dividido en secciones, las que asumen tareas específicas.
 
Declaración de Funciones
En esta sección se encuentran definidas una serie de funciones, las cuales se utilizarán a posteriori en el código. Las funciones mencionadas incluyen la creación de un DataFrame a partir de un archivo JSON con ciertos errores de formato, el llenado de valores nulos en una columna con valores consecutivos, la estipulación de valores a partir de una columna de precios, la extracción de años y fechas de cadenas de texto, la limpieza de caracteres especiales, el análisis de sentimiento de texto y otras operaciones de procesamiento de datos.
 
Carga de Datos
Dentro de esta sección se encuentran cargados tres conjuntos de datos desde archivos JSON comprimidos. Los mismos se ajustan a información sobre juegos de Steam, revisiones de usuarios y datos de estos. Estos conjuntos de datos son: df_steam_games, df_user_reviews y df_users_items, respectivamente.
 
Transformaciónes en df_steam_games
Esta sección efectúa una serie de transformaciones en el conjunto de datos df_steam_games, entre las que se encuentran la eliminación de columnas irrelevantes, relleno de valores nulos, conversión de tipos de datos, extracción de años de fechas, limpieza de caracteres especiales y otras operaciones de limpieza y transformación de datos.
 
Análisis Univariado en df_steam_games
En esta instancia se encuentran realizados análisis univariados de las variables en df_steam_games. Nubes de palabras, gráficos de barras y diagramas de cajas son visualizaciones generadas para examinar las características de las variables numéricas y categóricas.
 
Análisis Multivariado en df_steam_games
En esta sección está ubicado el análisis multivariado en el conjunto de datos df_steam_games. Por lo que está calculada la matriz de correlación entre variables numéricas y los gráficos de dispersión e histogramas están generados para inspeccionar las relaciones entre variables.
 
Creación de Dataset genres y developer
Se obtiene información desanidada y limpia dentro de un nuevo conjunto de datos llamados genres creado a partir de la columna 'genres' en df_steam_games y otro llamado developer concebido a partir de la columna 'developer'
 
Transformaciones en df_user_reviews
Esta sección está destinada a realizar transformaciones en df_user_reviews, la cual incluye revisiones de usuarios. Se eliminan las columnas irrelevantes, se convierten fechas al formato que mejor se adecúa y se realiza un análisis del sentimiento en las revisiones.
 
Creación de Dataset users_items
A partir de la columna 'items' en df_users_items se ha creado users_items: un nuevo conjunto de datos que contiene información limpia y desanidada.
 
Análisis de Usuarios
La identificación de los usuarios con mayor tiempo jugado y los usuarios con mayor cantidad de ítems jugados, están incluidos en el análisis de usuarios.
 
Requerimientos
Para efectivizar la ejecución de este código, será necesario tener instaladas las bibliotecas de Python que se mencionan a continuación:
-          pandas
-          gzip
-          re
-          math
-          numpy
-          wordcloud
-          matplotlib
-          collections
-          seaborn
-          textblob
Estas bibliotecas pueden ser instaladas utilizando pip u otro gestor indistinto de paquetes de Python.
 
Uso del Código
El código se encuentra escindido en secciones, las cuales se ejecutan secuencialmente. De igual manera, se puede ejecutar el código de forma conjunta o realizarlo en secciones específicas de acuerdo con las necesidades del usuario.
Antes de ejecutar el código es primordial verificar que los archivos JSON comprimidos se encuentren en la ubicación especificada en el código.
 
Resultados
El código produce transformaciones en los conjuntos de datos, visualizaciones para explorar los datos y crea nuevos conjuntos de datos limpios y desanidados a partir de las columnas destacadas.
Los resultados comprenden conjuntos de datos tales como df_steam_games, df_user_reviews, genres, developer y users_items listos para su posterior análisis.
