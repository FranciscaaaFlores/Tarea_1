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

