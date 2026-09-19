import os
import cv2
import matplotlib.pyplot as plot
import numpy as np

ruta = os.path.join(os.path.dirname(__file__), "P2_IMG_2423.tif")
imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

#La función va a recibir la imagen, el alto y ancho de la región que se desea y la separación vertical y horizontal entre cada región.
#La separación se considera desde el borde de cada cuadrito
def regionesytransformacion(imagen, alto, ancho, sepvertical, sephorizontal, parametro):
    altoi = imagen.shape[0]
    anchoi = imagen.shape[1]
    altor = alto
    anchor = ancho

    #En el caso de que la imagen no pueda ser dividida exactamente por el alto o ancho de las regiones definidas se utilizará mirror padding (visto
    #en clases) para completar aquella región.
    restovertical = (altoi - altor) % sepvertical
    padvertical = 0 
    if restovertical != 0: #Si es que no se alcanza a completar una cantidad entera de regiones verticales:
        padvertical = sepvertical- restovertical #Se calcula lo necesario para completar la última región

    restohorizontal = (anchoi - anchor) % sephorizontal
    padhorizontal = 0 
    if restohorizontal != 0: #Si es que no se alcanza a completar una cantidad entera de regiones horizontales:
        padhorizontal = sephorizontal- restohorizontal #Se calcula lo necesario para completar la última región

    #Se crea la imagen con pixeles extra en sus bordes, en caso de haber tenido regiones exactas no se agrega nada
    imagenconzp = np.pad(imagen, ((0, padvertical), (0, padhorizontal)), mode="reflect")
    altoi = imagenconzp.shape[0]
    anchoi = imagenconzp.shape[1]

    #Se crea arreglo para almacenar las regiones, es decir, cada cuadrito formado por el alto y ancho definidos, considerando el solape
    regiones = [] 

    for v in range(0, altoi - altor + 1, sepvertical):
        for h in range(0, anchoi - anchor + 1, sephorizontal):
            cuadrito = imagenconzp[v: v + altor, h: h + anchor] #Creamos cada cuadro del tamaño definido
            regiones.append(cuadrito)

    #Para utilizar la fórmula de T vista en clases, definimos los parámetros M, N y L
    dimcuadrito = regiones[0] #Tomamos un cuadrito para determinar las dimensiones (puesto que todos tienen las mismas)
    M = dimcuadrito.shape[0] #Pixeles de alto
    N = dimcuadrito.shape[1] #Pixeles de ancho
    L = 256 #Niveles de gris

    #Creamos arreglo para almacenar las transformaciones de los cuadritos

    identidad = np.arange(256)
    transformaciones = []
    for cuadrito in regiones:
        nj = np.histogram(cuadrito, bins = 256, range=(0, 256))[0]
        sumanj = np.cumsum(nj)
        #Fórmula vista en clases para ecualización del histograma
        T = ((L-1)/(M*N)) * sumanj #Aqui hay decimales, hay que pasarlos a enteros entre 0 y 255
        Tm = T * parametro + (1 - parametro) * identidad #Aquí se implementó el mecanismo de control de contraste
        #en donde si parametro = 0, obtenemos la imagen original sin cambios, y parametro = 1 es la imagen
        #ecualizada totalmente.
        T2 = (np.round(Tm)).astype(np.uint8)
        transformaciones.append(T2)

    #Creamos otro arreglo, esta vez para los cuadritos con la transformación aplicada
    cuadritosecualizados = []
    for i in range(len(regiones)):
        cuadritoantes = regiones[i] #Tomamos cada cuadrito
        transformacionrespectiva = transformaciones[i] #Con su respectiva transformación
        cuadritotransformado = transformacionrespectiva[cuadritoantes] #Se le asigna a cada cuadrito el valor después de la transformación
        cuadritosecualizados.append(cuadritotransformado)

    #Una vez que tenemos todos los cuadritos en el arreglo de regiones con sus nuevos valores podemos formar la imagen nuevamente
    #Debido al solapamiento, habrán pixeles con más de un valor de intensidad, imagen1 considera esto a la vez que tenemos un arreglo cs que
    #almacenará las veces que se le sumaron diferentes valores
    imagen1 = np.zeros((altoi, anchoi))
    cs = np.zeros((altoi, anchoi))

    i = 0
    for v in range(0, altoi - altor + 1, sepvertical):
        for h in range(0, anchoi - anchor + 1, sephorizontal):
            cuadrito = cuadritosecualizados[i]
            imagen1[v: v + altor, h: h + anchor] += cuadrito
            cs[v: v + altor, h: h + anchor] += 1
            i += 1

    #Se hace una "normalización" la que considera el valor de cada pixel y las veces que se incluyó para calcular diferentes regiones
    imagen2 = imagen1 / cs
    #Para obtener la imagen ecualizada finalmente se debe considerar la posibilidad de que se le hayan agregado pixeles por el padding, por lo que
    #la imagen final debe tener las mismas dimensiones que la imagen original.
    imagenecualizada = (imagen2[: imagen.shape[0], : imagen.shape[1]]).astype(np.uint8)

    return imagenecualizada

#________________________gráfica____________________________________________

#En caso de que se quiera la ecualización global clásica, se entregan como parámetos de la función altoi/anchoi/sepv/seph
altoi = imagen.shape[0] 
anchoi= imagen.shape[1]
sepv = imagen.shape[0]
seph = imagen.shape[1]
imagenresultado = regionesytransformacion(imagen, alto = int(altoi/16), ancho = int(anchoi/16), sepvertical= int(altoi/128), sephorizontal=  int(anchoi/128), parametro= 0.8)
plot.figure(figsize=(10, 5))
plot.subplot(1, 2, 1)
plot.imshow(imagen, cmap="gray")
plot.xlabel(
    f"Alto región = {altoi}\n"
    f"Ancho región = {anchoi}\n", fontsize=12)
plot.title("Original", fontsize=15)

plot.subplot(1, 2, 2)
plot.imshow(imagenresultado, cmap="gray")
plot.xlabel(
    f"Alto región = {int(altoi/16)}\n"
    f"Ancho región = {int(anchoi/16)}\n"
    f"Sep. Vertical = {int(altoi/128)}\n"
    f"Sep. Horizontal = {int(anchoi/128)}\n"
    "Mezcla transformación con identidad = 0.8",  fontsize=12)
plot.title("Ecualización local", fontsize=15)

plot.tight_layout()
plot.show()
