import PixelMatrix
from math import sin, cos
from time import sleep
import numpy as np

import configparser
config = configparser.ConfigParser() 
config.read(r"../../../MatrixHost.ini")
HOST = config.get("Pixelserver","Host")
UDP_HOST = config.get("WLED Server","Host")

# Additive Farbmischung
# aus Rot, Grün und Blauanteil
Weiss = (255, 255, 255)
Rot   = (255, 0, 0)
Gruen = (0, 255, 0)
Blau  = (0, 0, 255)
Lila  = (200,100,200)


def Paddel(aArray : np.ndarray, x,y):
    for j in range(1,5):
        aArray[x+0][j+y] = Weiss
        aArray[x+1][j+y] = Weiss
def Ball(aArray : np.ndarray, x,y):
    aArray[x][y] = Weiss
    aArray[x][y+1] = Weiss
    aArray[x+1][y] = Weiss
    aArray[x+1][y+1] = Weiss


# Wir erzeugen eine Instanz Namens ,,Matrix``
# der Klasse PixelMatrix() aus der PixelMatrix Bibliothek
# Dies übernimmt für uns alles, was wir zum Pixeln brauchen.
# Wir müssen uns nun nur noch um das setzen der Pixel kümmern
Matrix = PixelMatrix.UdpPixelMatrix() #UDP_HOST
#Matrix = PixelMatrix.PixelMatrix(HOST)

Background = np.zeros(shape=(Matrix.Width,Matrix.Height,3), dtype=np.uint8)
for i in range(1,round(Matrix.Height/2)):
    Background[round(Matrix.Width/2)][i*2] = Weiss
Matrix.NdArray(Background)
Spielfeld = np.copy(Background)
sleep(1.6)
x = 30
y = 16
for i in range(1,Matrix.Width-2):
    Spielfeld = np.copy(Background)
    Ball(Spielfeld,i,10)
    Paddel(Spielfeld,1,5)
    Paddel(Spielfeld,Matrix.Width-2,5)

    Matrix.NdArray(Spielfeld)
    #Matrix.Putpixel(i,y+round(sin(i/9)*15), Gruen)
    #Matrix.Putpixel(x+round(cos(i/9)*15),int(i/2), Rot)
    #Matrix.Putpixel(x+round(cos(i/9)*15),y+round(sin(i/9)*15), Lila)
    sleep(0.05)


