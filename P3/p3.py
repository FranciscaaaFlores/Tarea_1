import os
import cv2
import matplotlib.pyplot as plot
import numpy as np
#Al igual que en las preguntas anteriores utilizamos las mismas librerías y la misma manera para cargar la imagen
ruta = os.path.join(os.path.dirname(__file__), "P3_IMG_2387_crop.tif")
imagen = cv2.imread(ruta) #en BGR
imagenrgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

