import os
import cv2
import matplotlib as plot
import numpy as np

ruta = os.path.join(os.path.dirname(__file__), "P2_IMG_2423.tif")
imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

#La función va a recibir la imagen, el alto y ancho de la región que se desea y la separación vertical y horizontal entre cada región.
#La separación se considera desde el borde de cada cuadrito
def regionesytransformacion(imagen, alto, ancho, sepvertical, sephorizontal):
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
    transformaciones = []
    for cuadrito in regiones:
        nj = np.histogram(cuadrito, bins = 256, range=(0,256))[0]
        sumanj = np.cumsum(nj)
        #Fórmula vista en clases para ecualización del histograma
        T = ((L-1)/(M*N)) * sumanj #Aqui hay decimales, hay que pasarlos a enteros entre 0 y 255
        T2 = (np.round(T)).astype(np.uint8)
        transformaciones.append(T2)
        print(T2)


altoi = imagen.shape[0]
anchoi= imagen.shape[1]
sepv = imagen.shape[0]
seph = imagen.shape[1]
regionesytransformacion(imagen, altoi, anchoi, altoi, anchoi )