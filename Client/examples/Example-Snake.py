import PixelMatrix
from time import sleep
import configparser
import keyboard
from random import random
from os import path

IniFile = "MatrixHost.ini" 
for _ in range (3):
    if path.exists(IniFile):
        break
    IniFile = "../" + IniFile

if path.exists(IniFile):
    config = configparser.ConfigParser() 
    config.read(IniFile)
    HOST = config.get("Pixelserver","Host")
    UDP_HOST = config.get("WLED Server","Host")
else:
    print("Inifile not found!")

# Additive Farbmischung
# aus Rot, Grün und Blauanteil
Weiss = (255, 255, 255)
Rot   = (255, 0, 0)
Gruen = (0, 255, 0)
Blau  = (0, 0, 255)
Lila  = (200,100,200)
Schwarz  = (0,0,0)

# Wir erzeugen eine Instanz Namens ,,Matrix``
# der Klasse PixelMatrix() aus der PixelMatrix Bibliothek
# Dies übernimmt für uns alles, was wir zum Pixeln brauchen.
# Wir müssen uns nun nur noch um das setzen der Pixel kümmern
#Matrix = PixelMatrix.UdpPixelMatrix()#UDP_HOST)
Matrix = PixelMatrix.PixelMatrix(HOST)
Matrix.Black()

my_list = [(0,0) for x in range(0, 10)]
apfel = (40,20)
pause = False 
length = 3
position = 0
queue = []
#Matrix.Putpixel(10,30, Weiss)
y = 21;
for i in range(14,60):
    kopf=(i,y)
    queue.append(kopf)
    if position < length:
        position += 1
    else:
        schwanz = queue.pop(0)
        Matrix.Putpixel(schwanz[0],schwanz[1],Schwarz)


    Matrix.Putpixel(apfel[0], apfel[1], Gruen)
    if kopf==apfel:
        length +=1
        apfel = (60*random(),33*random())
    Matrix.Putpixel(kopf[0],kopf[1], Blau)
    sleep(0.5)
    if keyboard.is_pressed('up'):
        y = y - 1
    if keyboard.is_pressed('down'):
        y = y + 1
   #if keyboard.is_pressed('left'):
       # y = y + 1 
    #if keyboard.is_pressed('right'):
       # y = y - 1
    if keyboard.is_pressed('esc'):
            pause = True
            sleep(3)
    while pause:
        if keyboard.is_pressed('esc'):
            pause = False
