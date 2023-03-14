"""
El siguiente código es un programa de Python que utiliza el marco de trabajo Flask
para crear un servidor web. El servidor web tiene dos rutas:
    1. /test_connection
    2. /verify_name.
La primera ruta es un punto final simple que devuelve un mensaje "OK" si el servidor
está en ejecución y accesible.
La segunda ruta se utiliza para verificar y corregir nombres malformados que se envían
a través de la URL.

El programa utiliza varias bibliotecas de Python, como re, numpy, pandas, Levenshtein y
metaphone, para llevar a cabo el procesamiento del nombre y la corrección.
"""
# Importamos las bibliotecas necesarias
import re                                           # Para trabajar con expresiones regulares.
import numpy as np                                  # Para trabajar con matrices y operaciones matemáticas.
import pandas as pd                                 # Para trabajar con estructuras de datos tabulares.
import Levenshtein                                  # Para calcular la distancia de Levenshtein entre cadenas de texto.
from metaphone import doublemetaphone               # Para obtener la versión fonética de una cadena de texto.
from flask import Flask, jsonify, request, Response # Para crear el servidor web y manejar las solicitudes HTTP.

# Leemos el archivo CSV que contiene el conjunto de datos de nombres que utilizaremos.
cDATASET_OF_NAMES = pd.read_csv("resources/export_full_dataset.csv")
# Definimos una expresión regular para buscar y eliminar caracteres repetidos en una cadena de texto.
cREGEX_NOT_REPEATED = re.compile(r"(.)\1+")
# Definimos una lista de consonantes en español.
# No se toma en cuenta la letra "Y", porque esta puede tomar el rol de vocal.
# En nombres como "Nataly", donde se usa como reemplazo de la vocal "i".
cCONSONANTS = "BCDFGHIJKLMNÑPQRSTVWXZ"

# Definimos una función para realizar el preprocesamiento de un token (nombre).
def pre_processing_token(iToken):
    # Convertimos todas las letras a mayúsculas y eliminamos caracteres repetidos.
    return cREGEX_NOT_REPEATED.sub(r"\1", iToken.upper())

# Definimos una función para obtener la versión semántica de un token (nombre).
def get_semantic_token(iToken):
    # Convertimos todas las letras a mayúsculas.
    vTokenRegex = iToken.upper()
    # Reemplazamos todas las consonantes en la cadena por la letra "C".
    vTokenRegex = vTokenRegex.translate(str.maketrans(cCONSONANTS, "C" * len(cCONSONANTS)))
    # Eliminamos caracteres repetidos
    vTokenRegex = cREGEX_NOT_REPEATED.sub(r"\1", vTokenRegex)
    return vTokenRegex

# Definimos una función para obtener el token correcto a partir de un token incorrecto
def get_correct_token(iToken):
    """ La función "get_correct_token" se encarga de obtener el token correcto a
        partir de un token incorrecto.
        Si el token incorrecto se encuentra en el conjunto de datos de nombres, se
        devuelve el token correspondiente y un valor de confianza igual a cero.
        Si el token no se encuentra en el conjunto de datos, se realiza una búsqueda
        utilizando el token preprocesado y se devuelve el token correspondiente y
        un valor de confianza igual.
    """
    # Buscamos el token en el conjunto de datos de nombres. Si existe salimos.
    vData = cDATASET_OF_NAMES[cDATASET_OF_NAMES["NAME"] == iToken.upper()]["NAME"].values.tolist()
    if len(vData) > 0:
        return vData[0], 0
    # Si no encontramos una coincidencia exacta, realizamos una búsqueda con el token preprocesado.
    vToken = pre_processing_token(iToken)
    vData = cDATASET_OF_NAMES[cDATASET_OF_NAMES["NAME"] == vToken]["NAME"].values.tolist()
    if len(vData) > 0:
        return vData[0], 0.3
    
    # Al trabajar en un ambiente descentralizado como la nube, no se puede
    # procesaar datos directamente sobre el DATASET original. Por riesgo de
    # bloqueos entre sessiones.
    vData = cDATASET_OF_NAMES.copy()
    
    # Obtenemos los fonemas del token, que indican su pronunciación.
    vMetaphoneA, vMetaphoneB = doublemetaphone(vToken)
    vMetaphoneB = vMetaphoneB if len(vMetaphoneB) > 0 else vMetaphoneA
    
    # Obtenemos el token semantico de como están distribuidas las consonantes
    # y vocales entre las palabras.
    vSemanticRegex = get_semantic_token(iToken)
    
    # Calculamos las distancias entre el token, sus fonemas y su expresión regular.
    vData["LEVENSHTEIN_TOKEN"]  = vData["NAME"].apply(lambda x : Levenshtein.distance(x, iToken))
    vData["LEVENSHTEIN_META_A"] = vData["METAPHONE_A"].apply(lambda x : Levenshtein.distance(x, vMetaphoneA))
    vData["LEVENSHTEIN_META_B"] = vData["METAPHONE_B"].apply(lambda x : Levenshtein.distance(x, vMetaphoneB))
    vData["LEVENSHTEIN_REGEX"]  = vData["REGEX_CV"].apply(lambda x : Levenshtein.distance(x, vSemanticRegex))
    
    # Calculamos la distancia total de sus cuatro ejes levensthein.
    vData["LEVENSHTEIN_TOTAL"] = np.power(vData["LEVENSHTEIN_TOKEN"], 2) + \
        np.power(vData["LEVENSHTEIN_META_A"], 2) + \
        np.power(vData["LEVENSHTEIN_META_B"], 2) + \
        np.power(vData["LEVENSHTEIN_REGEX"], 2)
    vData["LEVENSHTEIN_TOTAL"] = np.sqrt(vData["LEVENSHTEIN_TOTAL"])
    
    # Ordenamos el dataset por la distancia total más pequeña (el nombre más similar)
    # y seleccionamos el mejor resultado.
    vData = vData.sort_values(by = "LEVENSHTEIN_TOTAL", ascending=True)
    vList = vData[0:1][["NAME", "LEVENSHTEIN_TOTAL"]].values.tolist()[0]
    return vList[0], vList[1]

def verify_malformed_name(iMalformedName : str):
    """ Esta función toma una cadena de texto iMalformedName y la divide en tokens
        separados por espacios. Luego, procesa cada token individualmente utilizando
        la función get_correct_token para obtener el token correcto y la distancia de
        Levenshtein entre el token original y el token correcto. Finalmente, devuelve
        un diccionario que incluye tanto el texto original como el nuevo, así como una
        lista de los resultados de cada token individual.
    """
    # Dividimos el nombre malformado en tokens separados por espacios.
    vArrayTokens = iMalformedName.split(" ")
    # Inicializamos una lista vacía para los resultados de cada token.
    vResult = []
    # Procesamos cada token individualmente para obtener el token correcto
    # y la distancia de Levenshtein entre el token original y el token correcto.
    for vToken in vArrayTokens:
        vNewToken, vDistance = get_correct_token(vToken)
        vResult.append({
            "original_token": vToken,
            "new_token": vNewToken,
            "token_difference": vDistance 
        })
    # Agregamos los resultados en un diccionario que incluye tanto el texto original como el nuevo
    # así como una lista de los resultados de cada token individual.
    vResult = {
        "original_text": iMalformedName,
        "new_text": " ".join([x["new_token"] for x in vResult]),
        "distances": vResult
    }
    return vResult

# Importamos la biblioteca Flask.
app : Flask = Flask(__name__)

# Establecemos una ruta que se utilizará para comprobar la conexión.
@app.route("/test_connection")
def hello():
    # Devolvemos un mensaje de confirmación.
    return "OK"

# Establecemos una ruta para verificar un nombre mal escrito.
@app.route("/verify_name")
def verify_name():
    # IMPORTANT: SECURITY LAYER HERE.
    # Recibimos el nombre original como argumento desde la petición HTTP.
    vOriginalName : str = request.args.get("name", None)

    # Verificamos el nombre y obtenemos el resultado.
    vR : dict = verify_malformed_name(vOriginalName)

    # Creamos una respuesta en formato JSON con el resultado.
    vResponse : dict = {"status": "ok", "result": vR}
    vResponse : Response = jsonify(vResponse)
    # Añadimos un encabezado para permitir el acceso desde cualquier origen.
    vResponse.headers.add('Access-Control-Allow-Origin', '*')
    return vResponse

# Si se ejecuta este archivo, se inicia el servidor en modo de desarrollo.
if __name__ == "__main__":
    print("Server running in development mode.")
    app.run(debug = True)

# https://github.com/jvalhondo/spanish-names-surnames > License GLPI
# https://www.kaggle.com/datasets/migalpha/spanish-names?resource=download > License ODBL
# https://towardsdatascience.com/text-similarity-w-levenshtein-distance-in-python-2f7478986e75