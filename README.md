# T1 - Fundamentos de Procesamiento de Imágenes
En este repositorios se encuentran 3 carpetas (P1, P2, P3), en las cuales se encuentra un archivo .py que contiene el código. No se ha realizado la pregunta 4.
con los respectivos comentarios asociados a cada parte y el archivo (imagen) que se subió en canvas para cada pregunta. 

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
