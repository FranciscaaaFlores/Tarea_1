import os
import cv2
import matplotlib.pyplot as plot
import numpy as np

ruta = os.path.join(os.path.dirname(__file__), "P1_IMG_2402.tif")
imagen = cv2.imread(ruta) #En BGR
imagenrgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

print(imagenrgb)
plot.figure(figsize=(10, 5))
plot.imshow(imagenrgb)
plot.show()