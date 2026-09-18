import os
import cv2
import matplotlib.pyplot as plot
import numpy as np
#Para experimentación y análisis se incluyeron las siguientes dos librerías para experimentar con otras imágenes.
from skimage import data
from skimage.io import imsave

ruta = os.path.join(os.path.dirname(__file__), "P1_IMG_2402.tif")
imagen = cv2.imread(ruta) #En BGR
imagenrgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

imageneya= data.rocket() #en rgb

#Definimos la función solicitada, con los parámetros: imagenrgb, los puntos de contro y el modo (HS o CIE lch)
def ColorSaturation(imagenrgb, puntosdecontrol, modo):
    def g_m(parametro, mh):
        return parametro * mh
    
    #Primero es necesario tratar los puntos de control, para poder interpolar entre ellos. Esta es la interpolación lineal pedida en el enunciado.
    def interpolacion(valoresh, puntosdecontrol):
        puntos = sorted(puntosdecontrol) #Ordenamos la lista de puntos de control
        #Creamos dos arreglos para almacenar los valores de h y m respectivamente
        h = []
        m = []

        #Recorremos los puntos de control, guardando el primer valor en el arreglo h y el segundo en el arreglo de m
        for p in puntos:
            h.append(p[0])
            m.append(p[1])

        #Hay que considerar los puntos de los extremos para interpolar, en donde además hay que tener en cuenta la transición del rojo de 360 a 0.
        #Ej: en el caso de que se tuviera en 350 0.8 y en 10 0.1, se debe determinar el valor en 360/0, que esta a mitad de camino entre ambos. En este caso
        #particular, el valor en 360/0 corresponde al promedio de los 2 m (0.8 y 0.1). 
        #Si consideramos x los valores de los angulos e y los valores de m, la pendiente queda p = m1 - m2 / (a1 - a2), en donde lo de abajo corresponde
        #a la distancia entre los angulos, en el caso de antes sería 360 - 350 = 10 + 10 - 0 = 10, = 20 grados. Para cualquier punto entonces sería
        #p = m1 - m2 / ((360 - a2) + a1). Ya que se sabe cuanto va cambiando la pendiente a medida que avanzan los grados, podemos encontrar la pendiente
        #en 360/0 como pb = m2 + p (360 - a2). 

        #Lo anterior aplica solo si tenemos más de 1 punto de control:
        if len(puntosdecontrol) > 1:
            if h[0] > 0 and h[-1] < 360:
                a2 = h[-1]
                a1 = h[0]
                m2 = m[-1]
                m1 = m[0]

                d = (360 - a2) + a1
                p = (m1 - m2)/ d
                pb = m2 + p * (360 - a2)

                h.insert(0, 0.0)
                m.insert(0, pb)
                h.append(360)
                m.append(pb)

            elif h[0] == 0:#En el caso de que justo se ingrese un m para 0, ese m se copia para 360
                pb = m[0]
                h.append(360)
                m.append(pb)

            elif h[-1] == 360:#En el caso de que justo se ingrese un m para 360, ese m se copia para 0
                pb = m[-1]
                h.insert(0, 0.0)
                m.insert(0, pb)

            interpolar = np.interp(valoresh, h, m)
            return interpolar

        else:
            #En el caso de tener solo un punto de control, tomamos el m que nos entreguen e interpolamos de 0 a 360 con ese valor (que al final es
            #una línea recta horizontal)
            m = puntosdecontrol[0][1]
            h = [0, 360]
            vm = [m, m]
            interpolar = np.interp(valoresh, h, vm)
            return interpolar

    #Ahora podemos pasar a los modos: para el modo HS usaré el modelo de color HSV.
    if modo == "HS":
        imagenenhsv = cv2.cvtColor(imagenrgb, cv2.COLOR_RGB2HSV)
        #Separamos los componentes de la imagen en Hue, Saturation y Value, para luego centrarnos en H y S.
        H = (imagenenhsv[:, :, 0]).astype(np.float32) * 2 #Se organiza como filas, columnas y canales
        S = (imagenenhsv[:, :, 1]).astype(np.float32)/ 255 #Lo normalice para que quedará en valor de 0 a 1 y luego multiplicar por el m correspondiente
        V = imagenenhsv[:, :, 2] #No se toca, se mantiene sin modificación
        mh = interpolacion(H, puntosdecontrol)
        Sg = g_m(S, mh)
        S2 = (np.clip(Sg, 0, 1)) * 255 #Luego de multiplicar por m, np.clip controla que se respete el mínimo y el máximo (0 y 1). 
        HSV2 = cv2.merge([(H/2).astype(np.uint8) , S2.astype(np.uint8) , V]) #Volvemos a formar la imagen, ahora con los nuevos valores para el componente saturación.
        resultado = cv2.cvtColor(HSV2, cv2.COLOR_HSV2RGB)

    elif modo == "CIELch":
        #Recordamos que el espacio CIE lch se obtiene a partir del espacio CIE lab, por lo que obtenemos la imagen en este último espacio.
        imagencielab = cv2.cvtColor(imagenrgb, cv2.COLOR_RGB2LAB)
        #Separamos los componentes de la imagen en L, a y b.
        L = (imagencielab[:, :, 0])
        a = (imagencielab[:, :, 1]).astype(np.float32) - 128 #En documentación de la conversión de espacios de color se indica que a y b vienen con un desfase
        #de 128, por lo que para usarlos les restamos 128.
        b = (imagencielab[:, :, 2]).astype(np.float32) - 128

        #Usamos las fórmulas vistas en clases para calcular los parámetros de CIE L*c*h* a partir del CIE L*a*b*
        #Se pide modificar c y dejar L con h sin modificación. Para modificar c, modificaremos a y b con mh.
        c = np.sqrt(a**2 + b**2)
        h = np.degrees(np.arctan2(b,a)) % 360
        #arctan2 devuelve valores entre -180 y 180° por lo que el mod 360 permite obtener valores dentro del rango para h 0 a 360.

        mh = interpolacion(h, puntosdecontrol)
        ag = g_m(a, mh)
        bg = g_m(b, mh)
        a2 = np.clip(ag + 128, 0, 255).astype(np.uint8)
        b2 = np.clip(bg + 128, 0, 255).astype(np.uint8)
        Lab2 = cv2.merge([L, a2, b2]) #Volvemos a formar la imagen, ahora con los nuevos valores.
        resultado = cv2.cvtColor(Lab2, cv2.COLOR_LAB2RGB)

    return resultado
#_____________________________________prueba y gráfica________________

puntos = [(0, 0.2), (50, 0.2), (100, 0.2), (130, 2), (180, 2), (240, 2), (300, 2), (340, 0.2)] 
#p1 = ColorSaturation(imagenrgb, puntos, modo="HS")
#p2 = ColorSaturation(imagenrgb, puntos, modo="CIELch")

p1 = ColorSaturation(imageneya, puntos, modo="HS")
p2 = ColorSaturation(imageneya, puntos, modo="CIELch")

plot.figure(figsize=(12, 4))
plot.subplot(1, 3, 1)
#plot.imshow(imagenrgb)
plot.imshow(imageneya)
plot.title("Original RGB")

plot.subplot(1, 3, 2)
plot.imshow(p1)
plot.title("Modo HS")

plot.subplot(1, 3, 3)
plot.imshow(p2)
plot.title("Modo CIE L*c*h*")

plot.tight_layout()
plot.show()


    


