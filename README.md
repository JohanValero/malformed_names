# malformed_names

## Double Metaphone
Double Metaphone es un algoritmo fonético que se utiliza para encontrar palabras que suenan de manera similar, pero que pueden estar escritas de forma diferente. El algoritmo fue desarrollado por Lawrence Philips y está diseñado para manejar las peculiaridades de la pronunciación en inglés, pero también funciona para otros idiomas.

Double Metaphone utiliza dos claves fonéticas para cada palabra, una para la pronunciación original y otra para una posible alternativa. Esto significa que es posible buscar palabras que suenan similares, pero que pueden tener diferentes ortografías.

Nota: Es importante tener en cuenta que Double Metaphone no es perfecto y puede generar claves fonéticas diferentes para palabras que suenan de manera similar. Por lo tanto, siempre debes verificar manualmente las palabras sugeridas para asegurarte de que sean correctas.

## Algoritmo Fuzzy
El algoritmo Fuzzy es un algoritmo de coincidencia de patrones que se utiliza para encontrar patrones similares en una cadena de texto. El algoritmo compara dos cadenas de texto y devuelve una puntuación que indica la similitud entre ellas.

El algoritmo Fuzzy se basa en el principio de que dos cadenas de texto son más similares si tienen más caracteres en común y si los caracteres están en el mismo orden.

Nota: Es importante tener en cuenta que el algoritmo Fuzzy también puede devolver una puntuación alta para cadenas de texto que no son realmente similares. Por lo tanto, siempre debes verificar manualmente las sugerencias para asegurarte de que sean correctas.

## Double Metaphone y Algoritmo Fuzzy

Para utilizar Double Metaphone y el algoritmo Fuzzy juntos, primero debes obtener las claves fonéticas de la palabra que deseas corregir utilizando Double Metaphone. Luego, puedes comparar cada clave fonética con las claves fonéticas de las palabras en una lista de nombres posibles utilizando el algoritmo Fuzzy.

Nota: Es importante tener en cuenta que Double Metaphone y el algoritmo Fuzzy no siempre encontrarán la corrección de nombres correcta. Siempre debes verificar manualmente las sugerencias para asegurarte de que sean correctas. Además, esta técnica es especialmente útil para corregir errores ortográficos comunes, pero puede ser menos efectiva para nombres con errores más complejos.

Ejemplo, el nombre "Jjhohaan" se podrá traducir con el metaphone JHN, quue corresponde a nombres como:
+ JOHAN
+ JOHANNA
+ JIHANE
+ ZHIHAN
+ JEHAN

Siendo JOHAN el más cercano para el valor ingresado.

Se recomienda usar metaphones mayores o iguales que el 90% para permitir que en caso de errores tipograficos que modifiquen el metaphone permita tenerlos en consideración por en caso de ingresar el nombre mal escrito "jojan" con el metaphone "JJN" (en extremo similiar a metaphone de "JHN") las opciones se convierten en una perdida parcial de información:
+ GIJON
+ JIAJUN
+ ZHIJIAN
+ JIA JUN
+ ZHIJUN

Tambien se puede optar por un por una busqueda de dos ejes, siendo los nombres con mayor correspondencia FUZZY por escritura y mayor correspondica FUZZY por metaphone. Tomando la curva con mayor corcondancia en ambos ejes.