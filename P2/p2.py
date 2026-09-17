import os
import cv2
import matplotlib as plot
import numpy as np

ruta = os.path.join(os.path.dirname(__file__), "P2_IMG_2423.tif")
imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
