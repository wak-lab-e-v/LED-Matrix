import PixelMatrix
from time import sleep
import configparser
import keyboard
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
Schwarz  = (0,0,0)

# Wir erzeugen eine Instanz Namens ,,Matrix``
# der Klasse PixelMatrix() aus der PixelMatrix Bibliothek
# Dies übernimmt für uns alles, was wir zum Pixeln brauchen.
# Wir müssen uns nun nur noch um das setzen der Pixel kümmern
Matrix = PixelMatrix.UdpPixelMatrix()#UDP_HOST)
#Matrix = PixelMatrix.PixelMatrix(HOST)
Matrix.Black()

my_list = [(0,0) for x in range(0, 10)]

#Matrix.Putpixel(10,30, Weiss)
y = 21;
for i in range(14,60):
    Matrix.Putpixel(i,y, Blau)
    Matrix.Putpixel(i-8,y, Schwarz)
    sleep(0.5)
    if keyboard.is_pressed('up'):
        y = y - 1
    if keyboard.is_pressed('down'):
        y = y + 1
        
    




