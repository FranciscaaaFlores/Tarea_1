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

#print(imagenrgb.shape) #Vemos que la imagen rgb tiene de salida (1908, 1827, 3) indicando los 3 canales 
#print(imagenegrises.shape) #Vemos que la imagen en escala de grises tiene de salida (427, 640) 
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
    #Definimos una función para la interpolación de Vecino más cercano, la cual recibe el parámetro al que se le quiere
    #aplicar la interpolación y sigue la fórmula vista en clases
    imagenf = imagen.astype(np.float32)
    def VCM(parametro, limite):
        if parametro - np.floor(parametro) < 0.5:
            p =  int(np.floor(parametro))
        else:
            p =  int(np.floor(parametro)) + 1

        if p < 0:
            return 0
        if p > limite:
            return limite
        return p


    #Ahora implementamos una función para la interpolación bilineal, asignamos los parámetros que utilizaremos (x, y, imagen) y usamos las fórmulas vistas en clases:
    def Bilineal(xc, yc, imagen):
        x = int(np.floor(xc))
        y = int(np.floor(yc))

        #Tuve que cambiar todos los np.clip por if/elif/else debido a que todo el programa estaba demasiado lento, se demoraba más de 6
        # minutos en dar las dos imágenes rgb interpoladas. Se logró reducir hasta 3,75 minutos aprox con s = 2 (imagen rgb: 45 segundos en modo VMC
        #y aprox 3 minutos en modo bilineal)
        if x < 0:
            x1 = 0
        elif x > anchoi - 1:
            x1 = anchoi - 1
        else:
            x1 = x

        if (x + 1) < 0:
            x2 = 0
        elif (x + 1) > anchoi - 1:
            x2 = anchoi - 1
        else:
            x2 = x + 1

        if y < 0:
            y1 = 0
        elif y > altoi - 1:
            y1 = altoi - 1
        else:
            y1 = y

        if (y + 1) < 0:
            y2 = 0
        elif (y + 1) > altoi - 1:
            y2 = altoi - 1
        else:
            y2 = y + 1
    
        f11 = imagen[y1, x1]#Es fila, columna (entonces y, x)
        f12 = imagen[y2, x1]
        f21 = imagen[y1, x2]
        f22 = imagen[y2, x2]
        d1 = (x2 - x1)
        d2 = (y2 - y1)

        if d1 == 0:
            d1 = 1
        if d2 == 0:
            d2 = 1

        fy1 = f11 + ((f21 - f11)/d1) * (xc - x1)
        fy2= f12 + ((f22 - f12)/d1) * (xc - x1)
        fxy = fy1 + ((fy2 - fy1)/d2) * (yc - y1)

        if fxy < 0:
            return 0
        if fxy > 255:
            return 255
        return fxy
    
    if modo == "VMC": #Interpolación vecino más cercano
        if len(imagen.shape) == 3: #Imagen RGB
            #Su imagen de salida tiene forma (nuevoalto, nuevoancho, 3)
            imagensalida= np.zeros((nuevoalto, nuevoancho, 3), np.uint8)
            #Recorremos los pixeles de la imagen de salida aplicando la transformación y la interpolación
            for yprima in range(nuevoalto):
                y = VCM(yprima/s, altoi - 1)
                if yprima % 200 == 0:
                    print("Fila", yprima, "de", nuevoalto)
                for xprima in range(nuevoancho):
                    x = VCM(xprima/s, anchoi - 1)
                    imagensalida[yprima, xprima, 0] = imagen[y, x, 0]
                    imagensalida[yprima, xprima, 1] = imagen[y, x, 1]
                    imagensalida[yprima, xprima, 2] = imagen[y, x, 2]

        elif len(imagen.shape) == 2: #Imagen en escala de grises
            #Su imagen de salida tiene forma (nuevoalto, nuevoancho)
            imagensalida= np.zeros((nuevoalto, nuevoancho), np.uint8)
            for yprima in range(nuevoalto):
                y = VCM(yprima/s, altoi - 1)
                if yprima % 200 == 0:
                    print("Fila", yprima, "de", nuevoalto)
                for xprima in range(nuevoancho):
                    x = VCM(xprima/s, anchoi -1)
                    imagensalida[yprima, xprima] = imagen[y, x]

    elif modo == "Bilineal":#Interpolación bilineal
        if len(imagen.shape) == 3: 
            imagensalida= np.zeros((nuevoalto, nuevoancho, 3), np.uint8)
            R = imagenf[: , :, 0]
            G = imagenf[: , :, 1]
            B = imagenf[: , :, 2]
            for yprima in range(nuevoalto):
                y = yprima / s
                if yprima % 200 == 0:
                    print("Fila", yprima, "de", nuevoalto)
                for xprima in range(nuevoancho):
                    x = xprima / s
                    imagensalida[yprima, xprima, 0] = int(Bilineal(x, y, R))
                    imagensalida[yprima, xprima, 1] = int(Bilineal(x, y, G))
                    imagensalida[yprima, xprima, 2] = int(Bilineal(x, y, B))

        elif len(imagen.shape) == 2:
            imagensalida= np.zeros((nuevoalto, nuevoancho), np.uint8)
            for yprima in range(nuevoalto):
                y = yprima / s
                if yprima % 200 == 0:
                    print("Fila", yprima, "de", nuevoalto)
                for xprima in range(nuevoancho):
                    x = xprima / s
                    imagensalida[yprima, xprima] = int(Bilineal(x, y, imagenf))

    return imagensalida

s = 0.5
#p1 = reescalaeinterpola(imagenrgb, s, "VMC")
#2 = reescalaeinterpola(imagenrgb, s, "Bilineal")
p3 = reescalaeinterpola(imagenegrises, s, "VMC")
p4 = reescalaeinterpola(imagenegrises, s, "Bilineal")
s2 = 2
p5 = reescalaeinterpola(p3, s2, "VMC")
p6 = reescalaeinterpola(p4, s2, "Bilineal")
plot.figure(figsize=(12,10))

plot.subplot(2, 2, (1,2))
plot.imshow(imagenegrises, cmap="gray")
plot.title("Imagen Original")

plot.subplot(2, 2, 3)
plot.imshow(p5, cmap="gray")
plot.title("Imagen en escala de grises, interpolación VMC")

plot.subplot(2, 2, 4)
plot.imshow(p6, cmap="gray")
plot.title("Imagen en escala de grises, interpolación Bilineal")
plot.subplots_adjust(hspace=0.7)
plot.tight_layout()

plot.figure(figsize=(12,10))

#plot.subplot(2, 2, (1,2))
#plot.imshow(imagenrgb)
#plot.title("Imagen Original")

#plot.subplot(2, 2, 3)
#plot.imshow(p1)
#plot.title("Imagen RGB, interpolación VMC")

#plot.subplot(2, 2, 4)
#plot.imshow(p2)
#plot.title("Imagen RGB, interpolación Bilineal")

plot.subplots_adjust(hspace=0.4)
plot.tight_layout()
plot.show()