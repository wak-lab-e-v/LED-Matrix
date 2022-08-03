import PixelMatrix
from math import sin, cos
from time import sleep
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

# Wir erzeugen eine Instanz Namens ,,Matrix``
# der Klasse PixelMatrix() aus der PixelMatrix Bibliothek
# Dies übernimmt für uns alles, was wir zum Pixeln brauchen.
# Wir müssen uns nun nur noch um das setzen der Pixel kümmern
#Matrix = PixelMatrix.UdpPixelMatrix() #UDP_HOST
Matrix = PixelMatrix.PixelMatrix(HOST)
Matrix.Black()
sleep(1.6)
x = 30
y = 16
for i in range(1,59):
    Matrix.Putpixel(i,y+round(sin(i/9)*15), Gruen)
    Matrix.Putpixel(x+round(cos(i/9)*15),int(i/2), Rot)
    Matrix.Putpixel(x+round(cos(i/9)*15),y+round(sin(i/9)*15), Lila)
    sleep(0.2)


