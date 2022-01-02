import PixelMatrix
from time import sleep
import configparser
config = configparser.ConfigParser() 
config.read(r"..\..\..\MatrixHost.ini")
HOST = config.get("Pixelserver","host")

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
#Matrix = PixelMatrix.UdpPixelMatrix()
Matrix = PixelMatrix.PixelMatrix(HOST)
Matrix.Black()

x = 0
y = 30
for i in range(1,31):
    Matrix.Putpixel(i,y-i, Weiss)


