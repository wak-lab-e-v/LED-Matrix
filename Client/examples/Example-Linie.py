import PixelMatrix
from time import sleep
import configparser
config = configparser.ConfigParser() 
config.read(r"../../MatrixHost.ini")
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
#Matrix = PixelMatrix.UdpPixelMatrix(UDP_HOST)
Matrix = PixelMatrix.PixelMatrix(HOST)
Matrix.Black()


#Matrix.Putpixel(10,30, Weiss)

for i in range(14,60):
    Matrix.Putpixel(i,21, Blau)
    Matrix.Putpixel(i-8,21, Schwarz)
    sleep(0.5)




