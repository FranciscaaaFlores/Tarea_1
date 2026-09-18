import os
import cv2
import matplotlib.pyplot as plot
import numpy as np
from skimage import data
from skimage.io import imsave
#Al igual que en las preguntas anteriores utilizamos las mismas librerías y la misma manera para cargar la imagen
ruta = os.path.join(os.path.dirname(__file__), "P3_IMG_2387_crop.tif")
imagen1 = cv2.imread(ruta) #en BGR
imagenrgb = cv2.cvtColor(imagen1, cv2.COLOR_BGR2RGB)

imagen2= data.rocket() #en rgb, la pasamos a escala de grises
imagenegrises= cv2.cvtColor(imagen2, cv2.COLOR_RGB2GRAY)

print(imagenrgb.shape) #Vemos que la imagen rgb tiene de salida (1908, 1827, 3) indicando los 3 canales 
print(imagenegrises.shape) #Vemos que la imagen en escala de grises tiene de salida (427, 640) 
def reescalaeinterpola(imagen, s, modo):
    #Debemos tratar el caso en que la imagen de entrada sea rgb o este en escala de grises. Sabemos que una imagen RGB esta formada ppor 3 matrices
    #(R, G y B) mientras que las imagenes en escala de grises no poseen estas 3 matrices sino una sola con los valores de intensidad del gris de 0 a 255
    #podemos utilizar .shape para saber cómo es la imagen de entrada.

    altoi = imagen.shape[0]
    anchoi = imagen.shape[1]
    nuevoalto = int(altoi * s) #int para asegurar que tanto alto y ancho sean enteros
    nuevoancho = int(anchoi * s)

    #De la clase de operatoria de imágenes e interpolación, si queremos hacer una transformación de escalamiento
    #x' = s * x , y' = s * y
    if modo == "VMC": #Interpolación vecino más cercano
        if len(imagen.shape) == 3: #Imagen RGB
            #Su imagen de salida tiene forma (nuevoalto, nuevoancho, 3)
            imagensalida= np.zeros((nuevoalto, nuevoancho, 3), np.uint8)

        elif len(imagen.shape) == 2: #Imagen en escala de grises
            #Su imagen de salida tiene forma (nuevoalto, nuevoancho)
            imagensalida= np.zeros((nuevoalto, nuevoancho), np.uint8)

    elif modo == "Bilineal":#Interpolación bilineal
        if len(imagen.shape) == 3: #Imagen RGB
            #Su imagen de salida tiene forma (nuevoalto, nuevoancho, 3)
            imagensalida= np.zeros((nuevoalto, nuevoancho, 3), np.uint8)

        elif len(imagen.shape) == 2: #Imagen en escala de grises
            #Su imagen de salida tiene forma (nuevoalto, nuevoancho)
            imagensalida= np.zeros((nuevoalto, nuevoancho), np.uint8)

    return imagensalida

#plot.figure(figsize=(12, 4))
#plot.imshow(imageng2, cmap = "gray")
#plot.title("Original")
#plot.show()
