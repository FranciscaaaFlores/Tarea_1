# T1 - Fundamentos de Procesamiento de Imágenes
En este repositorios se encuentran 3 carpetas (P1, P2, P3), en las cuales se encuentra un archivo .py que contiene el código con los respectivos comentarios asociados a cada parte y el archivo (imagen) que se subió en canvas para cada pregunta. No se ha realizado la pregunta 4.

Cabe recalcar que los códigos no cuentan con interfaz gráfica, por lo que para modificar los parámetros y llamar a las funciones se encuentran las líneas correspondientes en donde se pueden modificar sus valores. 

## P1 (Pregunta 1 — Saturación selectiva de color)
Esta pregunta implementa la función ColorSaturation que permite modificar de forma selectiva la saturación 
de una imagen RGB según su tono y un parámetro m. Dentro del código se implementa una función g_m, que en este caso
se define como la saturación original multiplicado por el factor m. De esta forma, una vez ingresados los puntos de control, se realiza una interpolación para aquellos tonos entre los puntos, obteniendo así una saturación selectiva controlada por el parámetro m. 

En esta pregunta se implementa la función ColorSaturation(imagenrgb, puntosdecontrol, modo), la cual recibe 3 parámetros: 
1. **"imagenRGB"**: Una imagen en formato RGB.
2. **"puntosdecontrol"**: Un arreglo de puntos de control de la forma [(..., ...), (..., ...), etc]
3. **"modo"**: Espacio de color en el que se quiere trabajar. Se debe ingresar "HS" si se quiere el Modo HS (el cual trabaja con el espacio HSV), y "CIELch" para trabajar con el espacio CIE L*c*h*.
   
### Cómo usar:
Para usarlo se pueden utilizar las imágenes que vienen dentro del código (que es el archivo de la T1 o bien una imagen de ski image). Basta con llamar a la función con los parámetros indicados para reproducir los resultados. 

### Resultados:
La salida del código es un Plot con 3 imágenes (Original, Modo HS, Modo CIE L*c*h*). 

## P2 (Pregunta 2 — Ecualización local y control de contraste)
Esta pregunta implementa un algoritmo de ecualización local de histograma para imágenes en escala de grises. Para hacer la ecualización local se definen mallas, es decir, se divide la imagen en regiones pequeñas, las que pueden solaparse o no. Es capaz de reproducir la ecualización global clásica si se entregan los parámetros adecuados (se especifica más abajo). 
Además, implementa un mecanismo de control de contraste que combina las transformaciones con la identidad. 

En esta pregunta se implementa la función regionesytransformacion(imagen, alto, ancho, sepvertical, sephorizontal, parametro), la cual recibe 6 parámetros:
1. **"imagen"**: Una imagen en escala de grises.
2. **"alto"**: El alto de las regiones que se desea crear.
3. **"ancho"**: El ancho de las regiones que se desea crear.
4. **"sepvertical"**: La separación vertical que se desea entre regiones. 
5. **"sephorizontal"**: La separación horizontal que se desea entre regiones. 
6. **"parametro"**: Para el mecanismo de control de contraste, toma valores entre 0 y 1 (en donde 0 equivale a no aplicar ninguna transformación y 1 a aplicar la transformación completa). Es la proporción en la que se combinan las transformaciones con la identidad.
 
### Cómo usar:
Para usarlo se pueden utilizar las imágenes que vienen dentro del código (que es el archivo de la T1 o bien una imagen de ski image pasándola a escala de grises). Basta con llamar a la función con los parámetros indicados para reproducir los resultados. 

### Resultados:
La salida original de este código es un plot con 2 imágenes (Original, ecualizada local). En el caso de la original se detallan sus dimensiones, de manera que es más sencillo visualizar las regiones. En el caso de la ecualizada local se detallan las dimensiones de las regiones, las separación vertical y horizontal, y el valor del parámetro de control de contraste.
Además, se encuentran comentados otros resultados desarrollados durante la implementación. De esta forma, se puede obtener un plot con 5 imágenes (si se descomentan las últimas subplot, procurando comentar las subplot originales), en las que se encuentran:
1. Imagen Original
2. Imagen ecualización global clásica (obtenida si se seleccionan los parámetros como: alto = alto imagen original, ancho =
   ancho imagen original, sepvertical = alto imagen original, sephorizontal = ancho imagen original, parámetro = 1). 
4. Imagen con ecualización local (en la que se pueden modificar sus regiones, parámetro = 1)
5. Imagen con mecanismo de contraste (en la que se pueden modificar sus regiones, parámetro distinto de 1)
6. Imagen con CLAHE (la tarea mencionaba que se podía usar implementar con fines comparativos únicamente, por lo que
   solo se usa con este propósito). Se puede modificar su clipLimit y el tamaño de las regiones.

Además, también se encuentra comentado el plot de un histograma y un gráfico de CDF. Esto se utilizó para analizar una sección homogénea de la imagen, por lo que si se quisiera usar se debe descomentar ambos gráficos y seleccionar la sección de imagen que se quiere analizar con estos gráficos. La salida es:
1. Histograma con la distrubución de los pixeles de la región a lo largo de los 255 niveles de gris.
2. Plot de CDF, con la suma acumulada del histograma a lo largo de los 255 niveles de gris.


## P3 (Pregunta 3 — Reescalado e interpolación bilineal)
En esta pregunta se implementa una función para reescalar una imagen mediante un factor s, lo que implica que se puede hacer una reducción o ampliación de la imagen. 

En esta pregunta se implementa la función reescalaeinterpola(imagen, s, modo), la que recibe 3 parámetros:
1. **"imagen"**: Una imagen en formato RGB o en escala de grises.
2. **"s"**: Un factor real s, que según lo indicado en la tarea se debe encontrar entre 0.5 y 2, sin embargo se hicieron pruebas con otros valores de s también. No hay problemas de código con menores a 0.5, pero entre mayor es S el tiempo de
ejecución de todo el programa es mucho mayor. Con respecto a esto, se han incluido unos print que indican en que fila de
la imagen va la implementación, de manera que se puede confirmar que se está ejecutando mientras se ve como progresa.
3. **"modo"**: Tipo de interpolación deseada, tiene dos opciones: "VMC" (Vecino más cercano) o "Bilineal" (interpolación bilineal.

### Cómo usar:
Para usarlo se pueden utilizar las imágenes que vienen dentro del código (que es el archivo de la T1 o bien una imagen de ski image, que en el caso del código se uso para comprobar el funcionamiento en imagenes de escala de grises). Basta con llamar a la función con los parámetros indicados para reproducir los resultados. 

### Resultados:
La salida de este código son 2 ventanas diferentes con 3 plots cada una. La primera ventana reproduce las 3 imágenes asociadas a la imagen RGB (Original, Interpolación vecino más cercano, Interpolación Bilineal). La segunda ventana reproduce las 3 imágenes asociadas a la imagen en escala de grises (Original, Interpolación vecino más cercano, Interpolación Bilineal). 
Dentro del código se implementaron unos print (que se encuentran comentados, en la función de interpolación bilineal) que fueron utilizados en una sección de preguntas guiadas. Si se descomentan estos generan como salida los valores para un píxel determinado, indicando coordenada de salida, coordenada de entrada, cuatro vecinos y valor interpolado. El píxel puede ser modificado en la línea correspondiente. 
