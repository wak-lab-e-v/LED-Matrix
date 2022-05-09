import PixelMatrix
from math import sin, cos, pi, trunc
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

def GRAD() -> float:
    return pi/180; 

def Paddel(aArray : np.ndarray, x,y):
    for j in range(1,5):
        aArray[x+0][j+y] = Weiss
        aArray[x+1][j+y] = Weiss
def Ball(aArray : np.ndarray, x,y):
    #print(x,y)
    aArray[x][y] = Weiss
    aArray[x][y+1] = Weiss
    aArray[x+1][y] = Weiss
    aArray[x+1][y+1] = Weiss


def RotateX(x,y,a) :
  return x*cos(a*pi/180)#-y*sin(a*pi/180);
    
def RotateY(x,y,a) :
  return x*sin(a*pi/180)#+y*cos(a*pi/180);


def Flieg(Von, Speed, Winkel):
    x = Von[0]+RotateX(Speed,0,Winkel)
    y = Von[1]+RotateY(Speed,0,Winkel)
    if x >= Matrix.Width-2:
       Winkel = 180 - Winkel*1.1; 
    if x < 0:
       Winkel = 0 - (Winkel*1.1-180);
    if y >= Matrix.Height-2:
       Winkel = -90 - (Winkel-90); 
    if y < 0:
       Winkel = 90 - (Winkel+90);
    #print(Winkel)
    x = Von[0]+RotateX(Speed,0,Winkel)
    y = Von[1]+RotateY(Speed,0,Winkel)

    return [x, y], Winkel
    

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


position = [15.0, 15.0]
angle    = 99
for i in range(1,1000):
    Spielfeld = np.copy(Background)
    Ball(Spielfeld,trunc(position[0]),trunc(position[1]))
    Paddel(Spielfeld,0,5)
    Paddel(Spielfeld,Matrix.Width-2,5)
    position, angle = Flieg(position, 1, angle)
    Matrix.NdArray(Spielfeld)
    #sleep(0.05)


